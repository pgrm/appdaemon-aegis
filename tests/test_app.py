"""Placeholder test file."""


def test_smoke_import():
    """Test that the package can be imported and has the expected members."""
    from appdaemon_aegis import AegisApp, __version__

    assert isinstance(__version__, str)
    assert AegisApp is not None
