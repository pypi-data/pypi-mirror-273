import dataclasses
import enum
import functools
import getpass
import os
import pathlib
from typing import Literal, Mapping, NamedTuple

import asyncssh


class ContainerRuntime(enum.Enum):
    """The container engine to use."""

    SINGULARITY = enum.auto()
    APPTAINER = enum.auto()
    DOCKER = enum.auto()
    PODMAN = enum.auto()

    @classmethod
    def from_string(
        cls, runtime: Literal["singularity", "apptainer", "docker", "podman"]
    ) -> "ContainerRuntime":
        return {
            "singularity": cls.SINGULARITY,
            "apptainer": cls.APPTAINER,
            "docker": cls.DOCKER,
            "podman": cls.PODMAN,
        }[runtime]

    def __str__(self):
        if self is self.SINGULARITY:
            return "singularity"
        elif self is self.APPTAINER:
            return "apptainer"
        elif self is self.DOCKER:
            return "docker"
        elif self is self.PODMAN:
            return "podman"
        else:
            raise NotImplementedError


class PublicKey(NamedTuple):
    algorithm: str
    key: str


@dataclasses.dataclass(frozen=True, kw_only=True)
class SlurmClusterConfig:
    name: str

    host: str
    host_public_key: PublicKey | None = None
    user: str | None = None
    port: int | None = None

    # Job submission directory
    cwd: str | None = None

    # Additional scripting
    prolog: str | None = None
    epilog: str | None = None

    # Job scheduling
    account: str | None = None
    partition: str | None = None
    qos: str | None = None

    # If true, a reverse proxy is initiated via the submission host.
    proxy: Literal["submission-host"] | str | None = None

    runtime: ContainerRuntime

    # Environment variables
    environment: Mapping[str, str] = dataclasses.field(default_factory=dict)

    # Mounts
    mounts: Mapping[os.PathLike[str] | str, os.PathLike[str] | str] = dataclasses.field(
        default_factory=dict
    )

    # Resource mapping
    resources: Mapping[str, "xm_slurm.ResourceType"] = dataclasses.field(default_factory=dict)  # type: ignore # noqa: F821

    def __post_init__(self) -> None:
        for src, dst in self.mounts.items():
            if not isinstance(src, (str, os.PathLike)):
                raise TypeError(
                    f"Mount source must be a string or path-like object, not {type(src)}"
                )
            if not isinstance(dst, (str, os.PathLike)):
                raise TypeError(
                    f"Mount destination must be a string or path-like object, not {type(dst)}"
                )

            if not pathlib.Path(src).is_absolute():
                raise ValueError(f"Mount source must be an absolute path: {src}")
            if not pathlib.Path(dst).is_absolute():
                raise ValueError(f"Mount destination must be an absolute path: {dst}")

    @functools.cached_property
    def ssh_known_hosts(self) -> asyncssh.SSHKnownHosts | None:
        if self.host_public_key is None:
            return None

        return asyncssh.import_known_hosts(
            f"[{self.host}]:{self.port} {self.host_public_key.algorithm} {self.host_public_key.key}"
        )

    @functools.cached_property
    def ssh_config(self) -> asyncssh.config.SSHConfig:
        ssh_config_paths = []
        if (ssh_config := pathlib.Path.home() / ".ssh" / "config").exists():
            ssh_config_paths.append(ssh_config)
        if (xm_ssh_config := os.environ.get("XM_SLURM_SSH_CONFIG")) and (
            xm_ssh_config := pathlib.Path(xm_ssh_config).expanduser()
        ).exists():
            ssh_config_paths.append(xm_ssh_config)

        config = asyncssh.config.SSHClientConfig.load(
            None,
            ssh_config_paths,
            True,
            getpass.getuser(),
            self.user or (),
            self.host or (),
            self.port or (),
        )

        if config.get("Hostname") is None:
            raise RuntimeError(
                f"Failed to parse hostname from host `{self.host}` using SSH configs: {', '.join(map(str, ssh_config_paths))}"
            )
        if config.get("User") is None:
            raise RuntimeError(
                f"Failed to parse user from SSH configs: {', '.join(map(str, ssh_config_paths))}"
            )

        return config

    @functools.cached_property
    def ssh_connection_options(self) -> asyncssh.SSHClientConnectionOptions:
        options = asyncssh.SSHClientConnectionOptions(config=None)
        options.prepare(last_config=self.ssh_config, known_hosts=self.ssh_known_hosts)
        return options

    def __hash__(self):
        return hash((
            self.host,
            self.user,
            self.port,
            self.cwd,
            self.prolog,
            self.epilog,
            self.account,
            self.partition,
            self.qos,
            self.proxy,
            self.runtime,
            frozenset(self.environment.items()),
        ))
