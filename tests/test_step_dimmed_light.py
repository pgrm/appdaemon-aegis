from __future__ import annotations

import json
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
    monkeypatch.setattr(instance, "listen_event", MagicMock())
    monkeypatch.setattr(instance, "listen_state", MagicMock())
    monkeypatch.setattr(instance, "run_in", MagicMock())
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
    publish_calls = light.mqtt.mqtt_publish.call_args_list
    config_call = next(
        (c for c in publish_calls if c[0][0] == "homeassistant/light/test_lamp_1/config"),
        None,
    )
    assert config_call is not None

    actual_payload = json.loads(config_call[0][1])
    expected_payload = {
        "name": "Test Lamp",
        "unique_id": "test_lamp_1",
        "schema": "json",
        "state_topic": "homeassistant/light/test_lamp_1/state",
        "command_topic": "homeassistant/light/test_lamp_1/set",
        "availability_topic": "homeassistant/light/test_lamp_1/availability",
        "payload_available": "online",
        "payload_not_available": "offline",
        "brightness": True,
        "brightness_scale": 255,
        "device": {
            "identifiers": ["test_lamp_1"],
            "name": "Test Lamp",
            "manufacturer": "AegisApp",
        },
    }
    assert actual_payload == expected_payload
    assert config_call.kwargs["retain"] is True


@pytest.mark.asyncio
async def test_command_handling_turn_off(light):
    """Test the turn-off command."""
    payload = LightCommandPayload(state="off")
    await light._handle_dimmer_command(payload)
    light.turn_off.assert_called_once_with("switch.test_light")


@pytest.mark.asyncio
async def test_command_handling_brightness_zero_turns_off(light):
    """Test that a brightness of 0 turns the light off."""
    payload = LightCommandPayload(brightness=0)
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

    light.light_handle.set_state.assert_called_once_with(brightness=255, state="on")


def test_abstract_setup():
    """Test that the abstract setup method raises NotImplementedError."""
    with pytest.raises(NotImplementedError):
        StepDimmedLight.setup(None)


def test_configure_no_object_id(light):
    """Test that an object_id is generated if not provided."""
    light.configure(
        friendly_name="Test Lamp",
        switch_entity="switch.test_light",
        level_provider="sensor.test_power",
    )
    assert light.light_handle.object_id == "ad_test_app_switch_test_light"


def test_configure_invalid_power_thresholds(light):
    """Test that configure raises ValueError for invalid power_thresholds."""
    with pytest.raises(ValueError):
        light.configure(
            friendly_name="Test Lamp",
            switch_entity="switch.test_light",
            level_provider="sensor.test_power",
            power_thresholds=[10.0],  # Should be 2 for 3 steps
        )


@pytest.mark.parametrize(
    "steps, expected_error",
    [
        ([], ValueError),
        ([0.1, 2], TypeError),
        ([0.1, 1.1], ValueError),
        ([10, 300], ValueError),
    ],
)
def test_normalize_steps_invalid(light, steps, expected_error):
    """Test that _normalize_steps raises errors for invalid inputs."""
    with pytest.raises(expected_error):
        light._normalize_steps(steps)


@pytest.mark.asyncio
async def test_get_current_power_level_callable_error(light):
    """Test _get_current_power_level with a callable that raises an error."""
    light.level_provider = AsyncMock(side_effect=Exception)
    assert await light._get_current_power_level() is None


@pytest.mark.asyncio
async def test_get_current_power_level_entity_error(light):
    """Test _get_current_power_level with an entity that returns an invalid state."""
    light.get_state.return_value = "unavailable"
    assert await light._get_current_power_level() is None


@pytest.mark.asyncio
async def test_update_and_publish_state_off(light):
    """Test _update_and_publish_state when the light is off."""
    light.get_state.return_value = "off"
    light.light_handle.set_state = MagicMock()
    await light._update_and_publish_state({})
    light.light_handle.set_state.assert_called_once_with(brightness=None, state="off")


@pytest.mark.asyncio
async def test_debounce_state_update(light):
    """Test the debouncing logic for state updates."""
    device_state = light.devices[light.light_handle.object_id]
    device_state.last_command_time = MagicMock()  # just needs to be not None

    # Last command was recent, so don't run the update
    light.datetime.return_value.__sub__.return_value.total_seconds.return_value = 1
    await light._debounce_state_update()
    light.run_in.assert_not_called()

    # Last command was long ago, so run the update
    light.run_in.reset_mock()
    light.datetime.return_value.__sub__.return_value.total_seconds.return_value = 10
    await light._debounce_state_update()
    light.run_in.assert_called_once()


@pytest.mark.parametrize(
    "current_index, target_index, num_levels, expected_flicks",
    [
        (-1, 0, 3, 1),  # Off to level 0
        (-1, 2, 3, 3),  # Off to level 2
        (0, 2, 3, 2),  # Level 0 to 2
        (2, 1, 3, 2),  # Level 2 to 1 (wraps around)
        (1, 1, 3, 0),  # Same level
    ],
)
def test_get_flicks(light, current_index, target_index, num_levels, expected_flicks):
    """Test the _get_flicks calculation."""
    light._brightness_levels = [0] * num_levels
    assert light._get_flicks(current_index, target_index) == expected_flicks


@pytest.mark.asyncio
async def test_perform_flicks(light):
    """Test the _perform_flicks method."""
    await light._perform_flicks(3)
    assert light.turn_off.call_count == 3
    assert light.turn_on.call_count == 3
    assert light.sleep.call_count == 6  # 2 calls per flick


@pytest.mark.asyncio
async def test_perform_flicks_zero(light):
    """Test that _perform_flicks does nothing for zero flicks."""
    await light._perform_flicks(0)
    light.turn_off.assert_not_called()
    light.turn_on.assert_not_called()
    light.sleep.assert_not_called()


def test_configure_generates_power_thresholds(light):
    """Test that power thresholds are generated if not provided."""
    light.configure(
        friendly_name="Test Lamp",
        switch_entity="switch.test_light",
        level_provider="sensor.test_power",
        steps=[100, 200],
    )
    assert light.power_thresholds == [150.0]


@pytest.mark.parametrize(
    "power, expected_level",
    [
        (None, -1),
        (5.0, 0),
        (15.0, 1),
        (25.0, 2),
    ],
)
def test_get_level_from_power(light, power, expected_level):
    """Test the _get_level_from_power calculation."""
    light.power_thresholds = [10.0, 20.0]
    assert light._get_level_from_power(power) == expected_level


@pytest.mark.parametrize(
    "brightness, expected_index",
    [
        (0, -1),
        (50, 0),
        (150, 1),
        (255, 2),
    ],
)
def test_get_level_from_brightness(light, brightness, expected_index):
    """Test the _get_level_from_brightness calculation."""
    light._brightness_levels = [64, 128, 255]
    assert light._get_level_from_brightness(brightness) == expected_index
