from importlib.metadata import PackageNotFoundError, packages_distributions, version

from .app import AegisApp

try:
    dist_name = packages_distributions()["appdaemon_aegis"][0]
    __version__ = version(dist_name)
except (PackageNotFoundError, KeyError):
    __version__ = "0.0.0"

__all__ = ("AegisApp", "__version__")
