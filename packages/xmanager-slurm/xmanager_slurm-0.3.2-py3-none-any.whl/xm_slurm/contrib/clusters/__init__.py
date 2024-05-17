import os

from xm_slurm import config, resources
from xm_slurm.contrib.clusters import drac

# ComputeCanada alias
cc = drac

__all__ = ["drac", "mila", "cc"]


def mila(
    *,
    user: str | None = None,
    partition: str | None = None,
    mounts: dict[os.PathLike[str] | str, os.PathLike[str] | str] | None = None,
) -> config.SlurmClusterConfig:
    """Mila Cluster (https://docs.mila.quebec/)."""
    if mounts is None:
        mounts = {
            "/network/scratch/${USER:0:1}/$USER": "/scratch",
            "/network/archive/${USER:0:1}/$USER": "/archive",
        }

    return config.SlurmClusterConfig(
        name="mila",
        user=user,
        host="login.server.mila.quebec",
        host_public_key=config.PublicKey(
            "ssh-ed25519",
            "AAAAC3NzaC1lZDI1NTE5AAAAIBTPCzWRkwYDr/cFb4d2uR6rFlUtqfH3MoLMXPpJHK0n",
        ),
        port=2222,
        runtime=config.ContainerRuntime.SINGULARITY,
        partition=partition,
        prolog="module load singularity",
        environment={
            "SINGULARITY_CACHEDIR": "$SCRATCH/.apptainer",
            "SINGULARITY_TMPDIR": "$SLURM_TMPDIR",
            "SINGULARITY_LOCALCACHEDIR": "$SLURM_TMPDIR",
            "SCRATCH": "/scratch",
            "ARCHIVE": "/archive",
        },
        mounts=mounts,
        resources={
            "rtx8000": resources.ResourceType.RTX8000,
            "v100": resources.ResourceType.V100,
            "a100": resources.ResourceType.A100,
            "a100l": resources.ResourceType.A100_80GIB,
            "a6000": resources.ResourceType.A6000,
        },
    )
