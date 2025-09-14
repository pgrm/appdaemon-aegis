from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _version
from typing import TYPE_CHECKING


def __getattr__(name: str):
    if name == "AegisApp":
        from .app import AegisApp as _AegisApp

        return _AegisApp
    raise AttributeError(name)


def __dir__():
    return sorted(list(globals().keys()) + ["AegisApp"])


if TYPE_CHECKING:
    # Make the symbol visible to static type checkers without importing at runtime
    from .app import AegisApp  # noqa: F401

try:
    __version__ = _version("appdaemon-aegis")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ("AegisApp", "__version__")
