from __future__ import annotations

import json
import traceback
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from datetime import datetime as datetime_type
from typing import Any, Dict, Literal, Optional
from uuid import UUID

from appdaemon.plugins.hass.hassapi import Hass

from .step_dimmed_lamp import StepDimmedLamp


class AegisApp(Hass, ABC):
    """Base class to intuitively write tested, reliable, and maintainable AppDaemon apps."""

    # --- Type hints for instance variables ---
    state_timer: Optional[UUID]
    mqtt: Any  # MQTT plugin API is not typed in AppDaemon
    lamp: StepDimmedLamp
    switch_entity: str
    flick_delay: float
    friendly_name: str
    object_id: str
    brightness: Optional[int]
    is_on: Optional[bool]
    last_mqtt_command_time: Optional[datetime_type]
    stabilization_time: int
    manual_debounce_time: int
    republish_on_confirm: bool
    base_topic: str
    config_topic: str
    state_topic: str
    command_topic: str
    availability_topic: str

    # Explicitly type the AppDaemon APIs that are used but not typed upstream.
    datetime: Callable[[], Awaitable[datetime_type]]

    def initialize(self) -> None:
        """Initialize the app, set up MQTT, and announce the device."""
        # --- Lamp Logic ---
        self.lamp = self.get_lamp_logic()

        # --- Timer for debouncing state updates ---
        self.state_timer = None

        # --- Get a handle to the MQTT Plugin API ---
        self.mqtt = self.get_plugin_api("MQTT")

        # --- Physical Device Entities ---
        self.switch_entity = self.args["switch_entity"]

        # --- Listen for physical state changes to debounce and publish ---
        self.listen_state(self.debounce_publish_state, self.switch_entity)
        if "current_sensor" in self.args:
            self.listen_state(self.debounce_publish_state, self.args["current_sensor"])

        self.log(f"Initializing '{self.name}' with arguments: {self.args}")

        # --- App-specific settings ---
        self.flick_delay = self.args.get("flick_delay", 0.055)
        self.friendly_name = self.args.get("friendly_name", "Dimmable Lamp")
        self.stabilization_time = self.args.get("stabilization_time", 5)
        self.manual_debounce_time = self.args.get("manual_debounce_time", 1)
        self.republish_on_confirm = self.args.get("republish_on_confirm", True)
        self.object_id = f"ad_{self.name}_{self.switch_entity}".replace(".", "_")

        # --- Temp Memory (only used for convenience) ---
        self.brightness = None
        self.is_on = None
        self.last_mqtt_command_time = None

        # --- MQTT Topics ---
        self.base_topic = f"homeassistant/light/{self.object_id}"
        self.config_topic = f"{self.base_topic}/config"
        self.state_topic = f"{self.base_topic}/state"
        self.command_topic = f"{self.base_topic}/set"
        self.availability_topic = f"{self.base_topic}/availability"

        # Announce the device and listen for commands
        self._announce_device()
        self.mqtt.mqtt_subscribe(self.command_topic)
        self.mqtt.listen_event(self._on_mqtt_command, "MQTT_MESSAGE")

        # Set initial availability and state
        self.mqtt.mqtt_publish(self.availability_topic, "online", retain=True)
        self.run_in(self.debounce_publish_state, 1)

        self.log(
            f"'{self.friendly_name}' initialized. "
            f"Listening for MQTT commands on {self.command_topic}"
        )

    @abstractmethod
    def get_lamp_logic(self) -> StepDimmedLamp:
        """Return the StepDimmedLamp instance for this app."""
        raise NotImplementedError

    @abstractmethod
    async def _get_current_level(self) -> Optional[int]:
        """Determine the current brightness level index from sensors."""
        raise NotImplementedError

    @abstractmethod
    async def _set_brightness(
        self, current_level_index: Optional[int], target_level_index: int
    ) -> None:
        """Perform the physical actions to change the brightness."""
        raise NotImplementedError

    def _announce_device(self) -> None:
        """Publish the MQTT discovery message for the light entity."""
        config_payload: Dict[str, Any] = {
            "name": self.friendly_name,
            "unique_id": self.object_id,
            "schema": "json",
            "state_topic": self.state_topic,
            "command_topic": self.command_topic,
            "availability_topic": self.availability_topic,
            "brightness": True,
            "brightness_scale": self.lamp.max_brightness,
            "device": {
                "identifiers": [self.object_id],
                "name": self.friendly_name,
                "manufacturer": "AppDaemon Aegis",
                "model": "MQTT Step-Dimmable Light",
            },
        }
        self.mqtt.mqtt_publish(
            self.config_topic, json.dumps(config_payload), retain=True
        )
        self.log("Published MQTT discovery message.")

    async def debounce_publish_state(self, *args: Any, **kwargs: Any) -> None:
        """Debounce state changes."""
        if (
            self.last_mqtt_command_time
            and (await self.datetime() - self.last_mqtt_command_time).total_seconds()
            < self.stabilization_time
        ):
            return

        if self.state_timer:
            self.cancel_timer(self.state_timer)

        self.state_timer = self.run_in(
            self.publish_state_callback, self.manual_debounce_time
        )

    async def _on_mqtt_command(
        self, event_name: str, data: Dict[str, Any], kwargs: Dict[str, Any]
    ) -> None:
        """Handle incoming MQTT commands."""
        if data.get("topic") != self.command_topic or "payload" not in data or not data["payload"]:
            return

        self.log(f"Received MQTT command: {data['payload']}")
        self.last_mqtt_command_time = await self.datetime()

        if self.state_timer:
            self.cancel_timer(self.state_timer)
            self.state_timer = None

        try:
            payload = json.loads(data["payload"])

            if "state" in payload and payload["state"].upper() == "OFF":
                self.is_on = False
                self.brightness = None
                await self.turn_off(self.switch_entity)
                await self._publish_state("OFF")
            else:
                self.is_on = True
                self.brightness = payload.get("brightness", self.lamp.max_brightness)
                target_level_index = self.lamp.get_level_from_brightness(self.brightness)
                is_off = await self.get_state(self.switch_entity) == "off"
                current_level_index = await self._get_current_level()

                await self._set_brightness(
                    None if is_off else current_level_index, target_level_index
                )
                await self._publish_state("ON", self.brightness)

            self.state_timer = self.run_in(
                self.publish_state_callback, self.stabilization_time
            )

        except json.JSONDecodeError:
            self.log(f"Invalid JSON in payload: {data['payload']}", level="WARNING")
        except Exception as e:
            tb_str = traceback.format_exc()
            self.log(f"Error in _on_mqtt_command: {e}\n{tb_str}", level="ERROR")

    async def publish_state_callback(self, kwargs: Dict[str, Any]) -> None:
        """Publish state to MQTT. This is now called by the debouncer."""
        self.state_timer = None
        await self._calculate_and_publish_state()

    async def _calculate_and_publish_state(self) -> None:
        """Calculate the authoritative state from sensors and publish it."""
        self.is_on = await self.get_state(self.switch_entity) == "on"

        if not self.is_on:
            if self.brightness is not None:
                self.brightness = None
                await self._publish_state("OFF", None)
            elif self.republish_on_confirm:
                await self._publish_state("OFF", None)
            return

        current_level_index = await self._get_current_level()

        if current_level_index is None or current_level_index == -1:
            if self.brightness is None:
                self.brightness = self.lamp.max_brightness
                await self._publish_state("ON", self.brightness)
            return

        last_known_level_index = (
            self.lamp.get_level_from_brightness(self.brightness)
            if self.brightness is not None
            else -1
        )

        if current_level_index == last_known_level_index:
            if self.republish_on_confirm:
                await self._publish_state("ON", self.brightness)
            return

        new_brightness = self.lamp.brightness_levels[current_level_index]
        self.brightness = new_brightness
        await self._publish_state("ON", self.brightness)

    async def _publish_state(
        self, state: Literal["ON", "OFF"], brightness: int | None = None
    ) -> None:
        """Helper to publish the state to MQTT."""
        state_payload: Dict[str, Any] = {"state": state}
        if brightness is not None:
            state_payload["brightness"] = brightness

        self.mqtt.mqtt_publish(self.state_topic, json.dumps(state_payload), retain=True)
        self.log(f"Published state: {state_payload}")

    def terminate(self) -> None:
        """Clean up by making the device unavailable on shutdown."""
        if self.state_timer:
            self.cancel_timer(self.state_timer)
            self.state_timer = None

        self.mqtt.mqtt_publish(self.availability_topic, "offline", retain=True)
        self.log("Set MQTT availability to offline.")
