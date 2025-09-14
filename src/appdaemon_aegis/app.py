from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from appdaemon.plugins.hass.hassapi import Hass

from .payloads import LightCommandPayload
from .types import StateType


@dataclass
class DeviceState:
    """Holds the state for a single managed device."""
    friendly_name: str
    command_callback: Callable[[LightCommandPayload], Awaitable[None]]
    state_payload: dict[str, str | int | bool] = field(default_factory=dict)
    last_command_time: datetime | None = None
    state_timer: UUID | None = None


class LightHandle:
    """A handle to a light device, returned by AegisApp.register_light."""

    def __init__(self, app: AegisApp, object_id: str):
        self._app = app
        self.object_id = object_id

    def set_state(self, brightness: int | None, state: StateType) -> None:
        """Set the state of the light device."""
        payload = {"state": state}
        if brightness is not None:
            payload["brightness"] = brightness
        self._app.publish_device_state(self.object_id, payload)

    @property
    def last_command_time(self) -> datetime | None:
        """The timestamp of the last command received for this device."""
        return self._app.devices[self.object_id].last_command_time


class AegisApp(Hass, ABC):
    """Abstract base class for creating reliable, code-centric AppDaemon apps."""

    # --- Framework instance variables ---
    # The MQTT plugin API is not typed in AppDaemon, so we use `Any`.
    mqtt: Any
    devices: dict[str, DeviceState]
    topic_to_object_id: dict[str, str]

    # --- Typing for AppDaemon APIs ---
    datetime: Callable[[], Awaitable[datetime]]

    def __init__(self, ad, name, logger, args, config, app_config, global_vars):
        super().__init__(ad, name, logger, args, config, app_config, global_vars)
        self.devices = {}
        self.topic_to_object_id = {}

    def initialize(self) -> None:
        """Initializes the app, calling subclass hooks for configuration and setup."""
        self.mqtt = self.get_plugin_api("MQTT")
        self.mqtt.listen_event(self._on_mqtt_command, "MQTT_MESSAGE")
        self.setup()
        self.log(f"AegisApp initialized with {len(self.devices)} device(s).")

    @abstractmethod
    def setup(self) -> None:
        """
        Subclasses must implement this method to configure the app and register devices.
        """
        raise NotImplementedError

    def register_light(
        self,
        object_id: str,
        friendly_name: str,
        command_callback: Callable[[LightCommandPayload], Awaitable[None]],
    ) -> LightHandle:
        """Registers a new light device with the framework."""
        if object_id in self.devices:
            raise ValueError(f"Device with object_id '{object_id}' already registered.")

        base_topic = f"homeassistant/light/{object_id}"
        config_topic = f"{base_topic}/config"
        command_topic = f"{base_topic}/set"
        availability_topic = f"{base_topic}/availability"

        self.devices[object_id] = DeviceState(
            friendly_name=friendly_name,
            command_callback=command_callback,
        )
        self.topic_to_object_id[command_topic] = object_id

        config_payload = {
            "name": friendly_name, "unique_id": object_id, "schema": "json",
            "state_topic": f"{base_topic}/state", "command_topic": command_topic,
            "availability_topic": availability_topic, "brightness": True,
            "brightness_scale": 255,
            "device": {"identifiers": [object_id], "name": friendly_name,
                       "manufacturer": "AegisApp"},
        }
        self.mqtt.mqtt_publish(config_topic, json.dumps(config_payload), retain=True)
        self.mqtt.mqtt_publish(availability_topic, "online", retain=True)
        self.mqtt.mqtt_subscribe(command_topic)

        self.log(f"Registered light '{friendly_name}' with command topic {command_topic}")
        return LightHandle(self, object_id)

    def publish_device_state(self, object_id: str, payload: dict[str, str | int | bool]) -> None:
        """Publishes the state for a specific device."""
        device = self.devices.get(object_id)
        if not device:
            return

        if device.state_payload == payload:
            return

        device.state_payload = payload
        base_topic = f"homeassistant/light/{object_id}"
        state_topic = f"{base_topic}/state"
        self.mqtt.mqtt_publish(state_topic, json.dumps(payload), retain=True)
        self.log(f"Published state for {object_id}: {payload}")

    async def _on_mqtt_command(
        self, event_name: str, data: dict[str, Any], kwargs: dict[str, Any]
    ) -> None:
        """
        Internal handler for all MQTT messages, dispatches to registered callbacks.
        The `data` and `kwargs` dicts are loosely typed as they come from AppDaemon's
        internal event bus and their contents can be dynamic.
        """
        topic = data.get("topic")
        object_id = self.topic_to_object_id.get(topic)
        if not object_id or not data.get("payload"):
            return

        device = self.devices[object_id]
        device.last_command_time = await self.datetime()

        try:
            payload = LightCommandPayload.from_json(data["payload"])
            await device.command_callback(payload)
        except Exception as e:
            self.log(f"Error in command callback for {object_id}: {e}", level="ERROR")

    def terminate(self) -> None:
        """Cleans up by making all registered devices unavailable."""
        for object_id in self.devices:
            base_topic = f"homeassistant/light/{object_id}"
            availability_topic = f"{base_topic}/availability"
            self.mqtt.mqtt_publish(availability_topic, "offline", retain=True)
        self.log("Set all registered devices to offline.")
