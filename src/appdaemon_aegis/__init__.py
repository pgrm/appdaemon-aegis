from importlib.metadata import version

from .app import AegisApp

__version__ = version("appdaemon-aegis")
__all__ = ("AegisApp", "__version__")
