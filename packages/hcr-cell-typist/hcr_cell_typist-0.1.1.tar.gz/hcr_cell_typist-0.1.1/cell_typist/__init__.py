from .core import load_qupath

try:
    from importlib.metadata import version as get_version, PackageNotFoundError
except ImportError:
    from pkg_resources import (
        get_distribution as get_version,
        DistributionNotFound as PackageNotFoundError,
    )

try:
    __version__ = get_version("hcr-cell-typist")
except PackageNotFoundError:
    __version__ = "0.0.0"
    print("Warning: Could not determine version. Defaulting to 0.0.0.")
