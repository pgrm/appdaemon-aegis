from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from appdaemon_aegis.payloads import LightCommandPayload
from appdaemon_aegis.step_dimmed_light import StepDimmedLight


class TestLight(StepDimmedLight):
    """A concrete light for testing, mimics a user's app."""

    # Override __init__ to be a no-op to isolate the logic for unit testing.
    def __init__(self):
        self.logger = MagicMock()

    @property
    def name(self) -> str:
        """Override the read-only name property for testing."""
        return "test_app"

    def setup(self):
        """Setup method that will be called by the test fixture."""
        self.configure(
            friendly_name="Test Lamp",
            switch_entity="switch.test_light",
            level_provider="sensor.test_power",
            object_id="test_lamp_1",
        )


@pytest.fixture
def light(monkeypatch) -> TestLight:
    """Provides a testable instance of the TestLight app."""
    # This fixture creates an instance of our test app and mocks all the
    # methods from the base Hass class that are called during initialization
    # and operation, allowing us to test the logic in isolation.
    instance = TestLight()

    # Mock the Hass methods that are called by the framework
    monkeypatch.setattr(instance, "get_plugin_api", lambda name: MagicMock())
    monkeypatch.setattr(instance, "listen_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(instance, "listen_state", lambda *args, **kwargs: None)
    monkeypatch.setattr(instance, "run_in", lambda *args, **kwargs: None)
    monkeypatch.setattr(instance, "turn_off", AsyncMock())
    monkeypatch.setattr(instance, "turn_on", AsyncMock())
    monkeypatch.setattr(instance, "sleep", AsyncMock())
    monkeypatch.setattr(instance, "get_state", AsyncMock(return_value="off"))
    monkeypatch.setattr(instance, "datetime", AsyncMock(return_value=MagicMock()))

    # Manually set the AD attribute that the log method needs
    instance.AD = MagicMock()
    instance.AD.config.ascii_encode = False

    # Manually initialize the device dictionaries that AegisApp.__init__ would create
    instance.devices = {}
    instance.topic_to_object_id = {}

    # Manually call initialize to trigger the app's setup() method
    instance.initialize()
    return instance


@pytest.mark.asyncio
async def test_setup_and_registration(light):
    """Test that the app sets up and registers the device correctly."""
    assert light.light_handle.object_id == "test_lamp_1"
    assert "test_lamp_1" in light.devices

    # Check that the MQTT registration was called with the correct config
    expected_payload = (
        '{"name": "Test Lamp", "unique_id": "test_lamp_1", "schema": "json", '
        '"state_topic": "homeassistant/light/test_lamp_1/state", '
        '"command_topic": "homeassistant/light/test_lamp_1/set", '
        '"availability_topic": "homeassistant/light/test_lamp_1/availability", '
        '"brightness": true, "brightness_scale": 255, '
        '"device": {"identifiers": ["test_lamp_1"], "name": "Test Lamp", '
        '"manufacturer": "AegisApp"}}'
    )
    light.mqtt.mqtt_publish.assert_any_call(
        "homeassistant/light/test_lamp_1/config",
        expected_payload,
        retain=True,
    )


@pytest.mark.asyncio
async def test_command_handling_turn_off(light):
    """Test the turn-off command."""
    payload = LightCommandPayload(state="OFF")
    await light._handle_dimmer_command(payload)
    light.turn_off.assert_called_once_with("switch.test_light")


@pytest.mark.asyncio
async def test_command_handling_set_brightness(light, monkeypatch):
    """Test setting a specific brightness level."""
    # Mock the state providers for this specific test
    light.get_state.return_value = "on"
    monkeypatch.setattr(light, "_get_current_power_level", AsyncMock(return_value=10.0))

    # Mock the _perform_flicks method to inspect its arguments
    monkeypatch.setattr(light, "_perform_flicks", AsyncMock())

    # Command to set brightness to max (level 2 for default steps)
    payload = LightCommandPayload(brightness=255)
    await light._handle_dimmer_command(payload)

    # Should go from level 0 to level 2, which is 2 flicks
    light._perform_flicks.assert_called_once_with(2)


@pytest.mark.asyncio
async def test_state_publishing(light, monkeypatch):
    """Test that the app correctly determines and publishes its state."""
    light.get_state.return_value = "on"
    monkeypatch.setattr(light, "_get_current_power_level", AsyncMock(return_value=200.0))

    # Mock the handle's set_state to verify it's called correctly
    light.light_handle.set_state = MagicMock()

    await light._update_and_publish_state({})

    light.light_handle.set_state.assert_called_once_with(brightness=255, state="ON")
