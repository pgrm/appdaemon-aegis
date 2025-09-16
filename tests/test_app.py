from __future__ import annotations

import logging
from unittest.mock import AsyncMock, MagicMock

import pytest

from appdaemon_aegis.app import AegisApp
from appdaemon_aegis.payloads import LightCommandPayload


class TestApp(AegisApp):
    """A concrete app for testing."""

    def __init__(self):
        """A no-op __init__ for testing."""
        self.logger = MagicMock()
        # The logger's log method is what's called internally by self.log()
        self.logger.log = MagicMock()

    @property
    def name(self) -> str:
        """Override the read-only name property for testing."""
        return "test_app"

    def setup(self) -> None:
        """A no-op setup for testing."""
        pass


@pytest.fixture
def app(monkeypatch) -> TestApp:
    """Provides a testable instance of the TestApp."""
    instance = TestApp()
    monkeypatch.setattr(instance, "get_plugin_api", lambda name: MagicMock())
    monkeypatch.setattr(instance, "listen_event", MagicMock())
    monkeypatch.setattr(instance, "datetime", AsyncMock(return_value=MagicMock()))

    # Manually set the AD attribute that the log method needs
    instance.AD = MagicMock()
    instance.AD.config.ascii_encode = False

    # Manually initialize the device dictionaries that AegisApp.__init__ would create
    instance.devices = {}
    instance.topic_to_object_id = {}

    instance.initialize()
    return instance


def test_smoke_import():
    """Test that the package can be imported and has the expected members."""
    from appdaemon_aegis import AegisApp, __version__

    assert isinstance(__version__, str)
    assert AegisApp is not None


def test_abstract_setup():
    """Test that the abstract setup method raises NotImplementedError."""
    with pytest.raises(NotImplementedError):
        AegisApp.setup(None)


def test_register_light_duplicate(app):
    """Test that registering a light with a duplicate object_id raises a ValueError."""
    app.register_light("light.test", "Test Light", AsyncMock())
    with pytest.raises(ValueError):
        app.register_light("light.test", "Test Light", AsyncMock())


def test_terminate(app):
    """Test that terminate unsubscribes from command topics."""
    app.register_light("light.test", "Test Light", AsyncMock())
    app.terminate()
    app.mqtt.mqtt_unsubscribe.assert_called_with("homeassistant/light/light.test/set")


@pytest.mark.asyncio
async def test_on_mqtt_command_invalid_payload(app, monkeypatch):
    """Test that _on_mqtt_command handles invalid payloads gracefully."""
    callback = AsyncMock()
    app.register_light("light.test", "Test Light", callback)
    monkeypatch.setattr(app, "datetime", AsyncMock())

    await app._on_mqtt_command(
        "MQTT_MESSAGE",
        {"topic": "homeassistant/light/light.test/set", "payload": "invalid-json"},
        {},
    )
    callback.assert_called_once_with(LightCommandPayload(state=None, brightness=None))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {"topic": "wrong_topic", "payload": "{}"},  # Topic not found
        {"payload": "{}"},  # Missing topic
        {"topic": "homeassistant/light/light.test/set"},  # Missing payload
    ],
)
async def test_on_mqtt_command_missing_data(app, data):
    """Test that _on_mqtt_command handles missing data."""
    callback = AsyncMock()
    app.register_light("light.test", "Test Light", callback)
    await app._on_mqtt_command("MQTT_MESSAGE", data, {})
    callback.assert_not_called()


@pytest.mark.asyncio
async def test_on_mqtt_command_callback_error(app, monkeypatch):
    """Test that _on_mqtt_command handles errors in the callback."""
    callback = AsyncMock(side_effect=Exception("test error"))
    app.register_light("light.test", "Test Light", callback)
    monkeypatch.setattr(app, "datetime", AsyncMock())

    await app._on_mqtt_command(
        "MQTT_MESSAGE",
        {"topic": "homeassistant/light/light.test/set", "payload": "{}"},
        {},
    )
    callback.assert_called_once()
    assert app.logger.log.call_args[0][0] == logging.ERROR
    assert app.logger.log.call_args[0][1] == "Error in command callback for light.test: test error"


def test_light_handle_last_command_time(app):
    """Test the last_command_time property of LightHandle."""
    handle = app.register_light("light.test", "Test Light", AsyncMock())
    now = MagicMock()
    app.devices["light.test"].last_command_time = now
    assert handle.last_command_time == now
    app.devices["light.test"].last_command_time = None
    assert handle.last_command_time is None
