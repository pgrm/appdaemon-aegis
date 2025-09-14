import importlib.metadata
from unittest.mock import patch

import pytest

import appdaemon_aegis


def test_getattr_unknown():
    """Test that __getattr__ raises AttributeError for unknown attributes."""
    with pytest.raises(AttributeError):
        _ = appdaemon_aegis.NonExistent


def test_getattr_aegis_app():
    """Test that AegisApp is lazy-loaded correctly."""
    from appdaemon_aegis.app import AegisApp as ImportedAegisApp

    assert appdaemon_aegis.AegisApp is ImportedAegisApp


def test_dir():
    """Test that __dir__ includes 'AegisApp'."""
    assert "AegisApp" in dir(appdaemon_aegis)


def test_version_not_found():
    """Test that __version__ is '0.0.0' when package is not found."""
    try:
        with patch(
            "importlib.metadata.version", side_effect=importlib.metadata.PackageNotFoundError
        ):
            # We need to reload the module to trigger the version check again
            importlib.reload(appdaemon_aegis)
        assert appdaemon_aegis.__version__ == "0.0.0"
    finally:
        # Reload again to restore the original version
        importlib.reload(appdaemon_aegis)
