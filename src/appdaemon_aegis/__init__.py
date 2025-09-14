from importlib.metadata import PackageNotFoundError, packages_distributions, version

from .app import AegisApp

try:
    __version__ = version("appdaemon-aegis")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ("AegisApp", "__version__")
