import asyncio
import collections.abc
import dataclasses
import functools
import hashlib
import logging
import operator
import re
import shlex
import typing
from typing import Any, Mapping, Sequence

import asyncssh
import backoff
import jinja2 as j2
from asyncssh.auth import KbdIntPrompts, KbdIntResponse
from asyncssh.misc import MaybeAwait
from xmanager import xm

from xm_slurm import batching, config, executors, status
from xm_slurm.console import console

SlurmClusterConfig = config.SlurmClusterConfig
ContainerRuntime = config.ContainerRuntime

"""
=== Runtime Configurations ===
With RunC:
    skopeo copy --dest-creds=<username>:<secret> docker://<image>@<digest> oci:<image>:<digest>

    pushd $SLURM_TMPDIR

    umoci raw unpack --rootless --image <image>:<digest> bundle/<digest>
    umoci raw runtime-config --image <image>:<digest> bundle/<digest>/config.json

    runc run -b bundle/<digest> <container-id>

With Singularity / Apptainer:

    apptainer build --fix-perms --sandbox <digest> docker://<image>@<digest>
    apptainer run --compat <digest>
"""

"""
#SBATCH --error=/dev/null
#SBATCH --output=/dev/null
"""

_POLL_INTERVAL = 30.0
_BATCHED_BATCH_SIZE = 16
_BATCHED_TIMEOUT = 0.2


class SlurmExecutionError(Exception): ...


class NoKBAuthSSHClient(asyncssh.SSHClient):
    """SSHClient that does not prompt for keyboard-interactive authentication."""

    def kbdint_auth_requested(self) -> MaybeAwait[str | None]:
        return ""

    def kbdint_challenge_received(
        self, name: str, instructions: str, lang: str, prompts: KbdIntPrompts
    ) -> MaybeAwait[KbdIntResponse | None]:
        del name, instructions, lang, prompts
        return []


def _group_by_ssh_options(
    ssh_options: Sequence[asyncssh.SSHClientConnectionOptions], job_ids: Sequence[str]
) -> dict[asyncssh.SSHClientConnectionOptions, list[str]]:
    jobs_by_cluster = collections.defaultdict(list)
    for options, job_id in zip(ssh_options, job_ids):
        jobs_by_cluster[options].append(job_id)
    return jobs_by_cluster


class _BatchedSlurmHandle:
    @functools.partial(
        batching.batch,
        max_batch_size=_BATCHED_BATCH_SIZE,
        batch_timeout=_BATCHED_TIMEOUT,
    )
    @staticmethod
    async def _batched_get_state(
        ssh_options: Sequence[asyncssh.SSHClientConnectionOptions], job_ids: Sequence[str]
    ) -> Sequence[status.SlurmJobState]:
        async def _get_state(
            options: asyncssh.SSHClientConnectionOptions, job_ids: Sequence[str]
        ) -> Sequence[status.SlurmJobState]:
            result = await get_client().run(
                options,
                [
                    "sacct",
                    "--jobs",
                    ",".join(job_ids),
                    "--format",
                    "JobID,State",
                    "--allocations",
                    "--noheader",
                    "--parsable2",
                ],
                check=True,
            )

            assert isinstance(result.stdout, str)
            states_by_job_id = {}
            for line in result.stdout.splitlines():
                job_id, state = line.split("|")
                states_by_job_id[job_id] = status.SlurmJobState.from_slurm_str(state)

            job_states = []
            for job_id in job_ids:
                if job_id in states_by_job_id:
                    job_states.append(states_by_job_id[job_id])
                # This is a stupid hack around sacct's inability to display state information for
                # array job elements that haven't begun. We'll assume that if the job ID is not found,
                # and it's an array job, then it's pending.
                elif re.match(r"^\d+_\d+$", job_id) is not None:
                    job_states.append(status.SlurmJobState.PENDING)
                else:
                    raise SlurmExecutionError(f"Failed to find job state info for {job_id}")
            return job_states

        jobs_by_cluster = _group_by_ssh_options(ssh_options, job_ids)

        job_states_per_cluster = await asyncio.gather(*[
            _get_state(options, job_ids) for options, job_ids in jobs_by_cluster.items()
        ])
        job_states_by_cluster: dict[
            asyncssh.SSHClientConnectionOptions, dict[str, status.SlurmJobState]
        ] = {}
        for options, job_states in zip(ssh_options, job_states_per_cluster):
            job_states_by_cluster[options] = dict(zip(jobs_by_cluster[options], job_states))

        job_states = []
        for options, job_id in zip(ssh_options, job_ids):
            job_states.append(job_states_by_cluster[options][job_id])
        return job_states

    @functools.partial(
        batching.batch,
        max_batch_size=_BATCHED_BATCH_SIZE,
        batch_timeout=_BATCHED_TIMEOUT,
    )
    @staticmethod
    async def _batched_cancel(
        ssh_options: Sequence[asyncssh.SSHClientConnectionOptions], job_ids: Sequence[str]
    ) -> Sequence[None]:
        async def _cancel(
            options: asyncssh.SSHClientConnectionOptions, job_ids: Sequence[str]
        ) -> None:
            await get_client().run(options, ["scancel", " ".join(job_ids)], check=True)

        jobs_by_cluster = _group_by_ssh_options(ssh_options, job_ids)
        return await asyncio.gather(*[
            _cancel(options, job_ids) for options, job_ids in jobs_by_cluster.items()
        ])


@dataclasses.dataclass(frozen=True, kw_only=True)
class SlurmHandle(_BatchedSlurmHandle):
    """A handle for referring to the launched container."""

    ssh_connection_options: asyncssh.SSHClientConnectionOptions
    job_id: str

    def __post_init__(self):
        if re.match(r"^\d+(_\d+|\+\d+)?$", self.job_id) is None:
            raise ValueError(f"Invalid job ID: {self.job_id}")

    @backoff.on_predicate(
        backoff.constant,
        lambda state: state in status.SlurmActiveJobStates,
        jitter=None,
        interval=_POLL_INTERVAL,
    )
    async def wait(self) -> status.SlurmJobState:
        return await self.get_state()

    async def stop(self) -> None:
        await self._batched_cancel(self.ssh_connection_options, self.job_id)

    async def get_state(self) -> status.SlurmJobState:
        return await self._batched_get_state(self.ssh_connection_options, self.job_id)


@functools.cache
def get_client() -> "Client":
    return Client()


@functools.cache
def get_template_env(container_runtime: ContainerRuntime) -> j2.Environment:
    template_loader = j2.PackageLoader("xm_slurm", "templates/slurm")
    template_env = j2.Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=False)

    def _raise_template_exception(msg: str) -> None:
        raise j2.TemplateRuntimeError(msg)

    template_env.globals["raise"] = _raise_template_exception
    template_env.globals["operator"] = operator

    match container_runtime:
        case ContainerRuntime.SINGULARITY | ContainerRuntime.APPTAINER:
            runtime_template = template_env.get_template("runtimes/apptainer.bash.j2")
        case ContainerRuntime.PODMAN:
            runtime_template = template_env.get_template("runtimes/podman.bash.j2")
        case _:
            raise NotImplementedError
    # Update our global env with the runtime template's exported globals
    template_env.globals.update(runtime_template.module.__dict__)

    return template_env


class Client:
    def __init__(self):
        self._connections: dict[
            asyncssh.SSHClientConnectionOptions, asyncssh.SSHClientConnection
        ] = {}
        self._connection_lock = asyncio.Lock()

    @backoff.on_exception(backoff.expo, asyncssh.Error, max_tries=5, max_time=60.0)
    async def _setup_remote_connection(self, conn: asyncssh.SSHClientConnection) -> None:
        # Make sure the xm-slurm state directory exists
        await conn.run("mkdir -p ~/.local/state/xm-slurm", check=True)

    async def connection(
        self,
        options: asyncssh.SSHClientConnectionOptions,
    ) -> asyncssh.SSHClientConnection:
        if options not in self._connections:
            async with self._connection_lock:
                try:
                    conn, _ = await asyncssh.create_connection(NoKBAuthSSHClient, options=options)
                    await self._setup_remote_connection(conn)
                    self._connections[options] = conn
                except asyncssh.misc.PermissionDenied as ex:
                    raise RuntimeError(f"Permission denied connecting to {options.host}") from ex
        return self._connections[options]

    @backoff.on_exception(backoff.expo, asyncssh.Error, max_tries=5, max_time=60.0)
    async def run(
        self,
        options: asyncssh.SSHClientConnectionOptions,
        command: xm.SequentialArgs | str | Sequence[str],
        *,
        check: bool = False,
        timeout: float | None = None,
    ) -> asyncssh.SSHCompletedProcess:
        client = await self.connection(options)
        if isinstance(command, xm.SequentialArgs):
            command = command.to_list()
        if not isinstance(command, str) and isinstance(command, collections.abc.Sequence):
            command = shlex.join(command)
        assert isinstance(command, str)
        logging.debug("Running command on %s: %s", options.host, command)

        return await client.run(command, check=check, timeout=timeout)

    async def template(
        self,
        *,
        job: xm.Job | xm.JobGroup,
        cluster: SlurmClusterConfig,
        args: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None,
        experiment_id: int,
        identity: str | None,
    ) -> str:
        if args is None:
            args = {}

        template_env = get_template_env(cluster.runtime)

        # Sanitize job groups
        if isinstance(job, xm.JobGroup) and len(job.jobs) == 1:
            job = typing.cast(xm.Job, list(job.jobs.values())[0])
        elif isinstance(job, xm.JobGroup) and len(job.jobs) == 0:
            raise ValueError("Job group must have at least one job")

        match job:
            case xm.Job() as job_array if isinstance(args, collections.abc.Sequence):
                template = template_env.get_template("job-array.bash.j2")
                sequential_args = [
                    xm.SequentialArgs.from_collection(trial.get("args", None)) for trial in args
                ]
                env_vars = [trial.get("env_vars") for trial in args]
                if any(env_vars):
                    raise NotImplementedError(
                        "Job arrays over environment variables are not yet supported."
                    )

                return template.render(
                    job=job_array,
                    cluster=cluster,
                    args=sequential_args,
                    env_vars=env_vars,
                    experiment_id=experiment_id,
                    identity=identity,
                )
            case xm.Job() if isinstance(args, collections.abc.Mapping):
                template = template_env.get_template("job.bash.j2")
                sequential_args = xm.SequentialArgs.from_collection(args.get("args", None))
                env_vars = args.get("env_vars", None)
                return template.render(
                    job=job,
                    cluster=cluster,
                    args=sequential_args,
                    env_vars=env_vars,
                    experiment_id=experiment_id,
                    identity=identity,
                )
            case xm.JobGroup() as job_group if isinstance(args, collections.abc.Mapping):
                template = template_env.get_template("job-group.bash.j2")
                sequential_args = {
                    job_name: {
                        "args": args.get(job_name, {}).get("args", None),
                    }
                    for job_name in job_group.jobs.keys()
                }
                env_vars = {
                    job_name: args.get(job_name, {}).get("env_vars", None)
                    for job_name in job_group.jobs.keys()
                }
                return template.render(
                    job_group=job_group,
                    cluster=cluster,
                    args=sequential_args,
                    env_vars=env_vars,
                    experiment_id=experiment_id,
                    identity=identity,
                )
            case _:
                raise ValueError(f"Unsupported job type: {type(job)}")

    @typing.overload
    async def launch(
        self,
        *,
        cluster: SlurmClusterConfig,
        job: xm.Job | xm.JobGroup,
        args: Mapping[str, Any] | None,
        experiment_id: int,
        identity: str | None = ...,
    ) -> SlurmHandle: ...

    @typing.overload
    async def launch(
        self,
        *,
        cluster: SlurmClusterConfig,
        job: xm.Job | xm.JobGroup,
        args: Sequence[Mapping[str, Any]],
        experiment_id: int,
        identity: str | None = ...,
    ) -> Sequence[SlurmHandle]: ...

    async def launch(
        self,
        *,
        cluster: SlurmClusterConfig,
        job: xm.Job | xm.JobGroup,
        args: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None,
        experiment_id: int,
        identity: str | None = None,
    ) -> SlurmHandle | Sequence[SlurmHandle]:
        # Construct template
        template = await self.template(
            job=job,
            cluster=cluster,
            args=args,
            experiment_id=experiment_id,
            identity=identity,
        )
        logging.debug("Slurm submission script:\n%s", template)

        # Hash submission script
        template_hash = hashlib.blake2s(template.encode()).hexdigest()[:8]

        conn = await self.connection(cluster.ssh_connection_options)
        async with conn.start_sftp_client() as sftp:
            # Write the submission script to the cluster
            # TODO(jfarebro): SHOULD FIND A WAY TO GET THE HOME DIRECTORY
            # INSTEAD OF ASSUMING SFTP PUTS US IN THE HOME DIRECTORY
            await sftp.makedirs(f".local/state/xm-slurm/{experiment_id}", exist_ok=True)
            async with sftp.open(
                f".local/state/xm-slurm/{experiment_id}/submission-script-{template_hash}.sh", "w"
            ) as fp:
                await fp.write(template)

        # Construct and run command on the cluster
        command = f"sbatch --chdir .local/state/xm-slurm/{experiment_id} --parsable submission-script-{template_hash}.sh"
        result = await self.run(cluster.ssh_connection_options, command)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to schedule job on {cluster.host}: {result.stderr}")

        assert isinstance(result.stdout, str)
        slurm_job_id, *_ = result.stdout.split(",")
        slurm_job_id = slurm_job_id.strip()

        console.log(
            f"[magenta]:rocket: Job [cyan]{slurm_job_id}[/cyan] will be launched on "
            f"[cyan]{cluster.name}[/cyan] "
        )

        if isinstance(job, xm.Job) and isinstance(args, collections.abc.Sequence):
            return [
                SlurmHandle(
                    ssh_connection_options=cluster.ssh_connection_options,
                    job_id=f"{slurm_job_id}_{array_index}",
                )
                for array_index in range(len(args))
            ]

        return SlurmHandle(
            ssh_connection_options=cluster.ssh_connection_options,
            job_id=slurm_job_id,
        )


@typing.overload
async def launch(
    *,
    job: xm.Job | xm.JobGroup,
    args: Mapping[str, Any],
    experiment_id: int,
    identity: str | None = ...,
) -> SlurmHandle: ...


@typing.overload
async def launch(
    *,
    job: xm.Job | xm.JobGroup,
    args: Sequence[Mapping[str, Any]],
    experiment_id: int,
    identity: str | None = ...,
) -> Sequence[SlurmHandle]: ...


async def launch(
    *,
    job: xm.Job | xm.JobGroup,
    args: Mapping[str, Any] | Sequence[Mapping[str, Any]],
    experiment_id: int,
    identity: str | None = None,
) -> SlurmHandle | Sequence[SlurmHandle]:
    match job:
        case xm.Job():
            if not isinstance(job.executor, executors.Slurm):
                raise ValueError("Job must have a Slurm executor")
            job_requirements = job.executor.requirements
            cluster = job_requirements.cluster
            if cluster is None:
                raise ValueError("Job must have a cluster requirement")

            return await get_client().launch(
                cluster=cluster,
                job=job,
                args=args,
                experiment_id=experiment_id,
                identity=identity,
            )
        case xm.JobGroup() as job_group:
            job_group_executors = set()
            job_group_clusters = set()
            for job_item in job_group.jobs.values():
                if not isinstance(job_item, xm.Job):
                    raise ValueError("Job group must contain only jobs")
                if not isinstance(job_item.executor, executors.Slurm):
                    raise ValueError("Job must have a Slurm executor")
                if job_item.executor.requirements.cluster is None:
                    raise ValueError("Job must have a cluster requirement")
                job_group_clusters.add(job_item.executor.requirements.cluster)
                job_group_executors.add(id(job_item.executor))
            if len(job_group_executors) != 1:
                raise ValueError("Job group must have the same executor for all jobs")
            if len(job_group_clusters) != 1:
                raise ValueError("Job group must have the same cluster for all jobs")

            return await get_client().launch(
                cluster=job_group_clusters.pop(),
                job=job,
                args=args,
                experiment_id=experiment_id,
                identity=identity,
            )
        case _:
            raise ValueError("Unsupported job type")
