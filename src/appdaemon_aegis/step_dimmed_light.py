from __future__ import annotations

from typing import Any
from uuid import UUID

from .app import AegisApp, LightHandle
from .payloads import LightCommandPayload
from .types import EntityId, LevelProvider


class StepDimmedLight(AegisApp):
    """
    A high-level AppDaemon app for creating a step-dimmable light.
    A user should inherit from this class and call `self.configure()`
    from within their `setup()` method.
    """

    # --- Instance variables to be populated by configure() ---
    light_handle: LightHandle
    switch_entity: EntityId
    level_provider: LevelProvider
    power_thresholds: list[float]
    flick_delay: float
    max_brightness: int
    _brightness_levels: list[int]

    # --- Debouncing Timers (not part of the central device state) ---
    _stabilization_time: int
    _manual_debounce_time: int
    _state_timer: UUID | None = None

    def configure(
        self,
        friendly_name: str,
        switch_entity: EntityId,
        level_provider: LevelProvider,
        object_id: str | None = None,
        steps: tuple[float] | tuple[int] = (0.25, 0.5, 1.0),
        power_thresholds: list[float] | None = None,
        flick_delay: float = 0.055,
        stabilization_time: int = 5,
        manual_debounce_time: int = 1,
        max_brightness: int = 255,
    ) -> None:
        """Configures the step-dimmable light."""
        if not object_id:
            object_id = f"ad_{self.name}_{switch_entity}".replace(".", "_")

        self.light_handle = self.register_light(
            object_id=object_id,
            friendly_name=friendly_name,
            command_callback=self._handle_dimmer_command,
        )

        self.switch_entity = switch_entity
        self.level_provider = level_provider
        self.flick_delay = flick_delay
        self._stabilization_time = stabilization_time
        self._manual_debounce_time = manual_debounce_time
        self.max_brightness = max_brightness
        self._brightness_levels = self._normalize_steps(steps)

        if power_thresholds:
            if len(power_thresholds) != len(self._brightness_levels) - 1:
                raise ValueError("power_thresholds must have one less element than steps.")
            self.power_thresholds = power_thresholds
        else:
            self.power_thresholds = self._generate_power_thresholds()

        self.listen_state(self._debounce_state_update, self.switch_entity)
        if isinstance(self.level_provider, EntityId):
            self.listen_state(self._debounce_state_update, self.level_provider)

    def setup(self) -> None:
        """
        A concrete implementation of a lamp must override this method
        and call `self.configure()` with its specific parameters.
        """
        raise NotImplementedError("You must implement setup() and call self.configure()")

    async def _handle_dimmer_command(self, payload: LightCommandPayload) -> None:
        """Handles a command from MQTT to change the light's state."""
        if payload.state and payload.state.upper() == "OFF":
            await self.turn_off(self.switch_entity)
            return

        target_brightness = self.max_brightness
        if payload.brightness is not None:
            target_brightness = payload.brightness
        target_index = self._get_level_from_brightness(target_brightness)

        is_off = await self.get_state(self.switch_entity) == "off"
        current_index = -1
        if not is_off:
            current_power = await self._get_current_power_level()
            current_index = self._get_level_from_power(current_power)

        num_flicks = self._get_flicks(current_index, target_index)
        await self._perform_flicks(num_flicks)

    async def _debounce_state_update(self, *args: Any, **kwargs: Any) -> None:
        """Debounces state changes for manual interactions."""
        if self._state_timer:
            self.cancel_timer(self._state_timer)

        # Use the handle to check the last command time for this specific device
        last_cmd_time = self.light_handle.last_command_time
        if last_cmd_time:
            time_since_cmd = (await self.datetime() - last_cmd_time).total_seconds()
            if time_since_cmd < self._stabilization_time:
                return

        self._state_timer = self.run_in(self._update_and_publish_state, self._manual_debounce_time)

    async def _update_and_publish_state(self, kwargs: dict[str, Any]) -> None:
        """Gets the authoritative state and publishes it via the handle."""
        self._state_timer = None
        is_on = await self.get_state(self.switch_entity) == "on"

        if not is_on:
            self.light_handle.set_state(brightness=None, state="OFF")
            return

        current_power = await self._get_current_power_level()
        level_index = self._get_level_from_power(current_power)

        brightness = self.max_brightness  # Fallback
        if level_index != -1:
            brightness = self._brightness_levels[level_index]

        self.light_handle.set_state(brightness=brightness, state="ON")

    # --- All the internal calculation logic ---
    async def _get_current_power_level(self) -> float | None:
        if isinstance(self.level_provider, EntityId):
            try:
                return float(await self.get_state(self.level_provider))
            except (ValueError, TypeError):
                return None
        else:
            try:
                return await self.level_provider()
            except Exception:
                return None

    def _normalize_steps(self, steps: tuple[float] | tuple[int]) -> list[int]:
        if not steps:
            raise ValueError("Steps cannot be empty.")
        normalized = []
        if all(isinstance(s, float) for s in steps):
            for s in steps:
                if not 0.0 <= s <= 1.0:
                    raise ValueError("Float steps must be between 0.0 and 1.0.")
                normalized.append(int(s * self.max_brightness))
        elif all(isinstance(s, int) for s in steps):
            for s in steps:
                if not 0 <= s <= self.max_brightness:
                    raise ValueError(f"Int steps must be between 0 and {self.max_brightness}.")
                normalized.append(s)
        else:
            raise TypeError("Steps must be a list of floats or a list of ints.")
        return sorted(normalized)

    def _generate_power_thresholds(self) -> list[float]:
        return [
            (self._brightness_levels[i] + self._brightness_levels[i + 1]) / 2.0
            for i in range(len(self._brightness_levels) - 1)
        ]

    def _get_level_from_power(self, power: float | None) -> int:
        if power is None:
            return -1
        for i, threshold in enumerate(self.power_thresholds):
            if power < threshold:
                return i
        return len(self.power_thresholds)

    def _get_level_from_brightness(self, brightness: int) -> int:
        if brightness <= 0:
            return -1
        return min(
            range(len(self._brightness_levels)),
            key=lambda i: abs(self._brightness_levels[i] - brightness),
        )

    def _get_flicks(self, current_index: int, target_index: int) -> int:
        num_levels = len(self._brightness_levels)
        if current_index == -1:
            return target_index + 1
        return (target_index - current_index + num_levels) % num_levels

    async def _perform_flicks(self, num_flicks: int) -> None:
        if num_flicks == 0:
            return
        for _ in range(num_flicks):
            await self.turn_off(self.switch_entity)
            await self.sleep(self.flick_delay)
            await self.turn_on(self.switch_entity)
            await self.sleep(self.flick_delay)
