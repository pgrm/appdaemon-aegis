from importlib.metadata import PackageNotFoundError, version as _version


def __getattr__(name: str):
    if name == "AegisApp":
        from .app import AegisApp as _AegisApp

        return _AegisApp
    raise AttributeError(name)


try:
    __version__ = _version("appdaemon-aegis")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ("AegisApp", "__version__")
