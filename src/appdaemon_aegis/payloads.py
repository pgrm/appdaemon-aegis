from __future__ import annotations

import json
from dataclasses import dataclass

from .utils import get_safe_brightness


@dataclass(frozen=True)
class LightCommandPayload:
    """A structured representation of a command payload for a light device."""

    state: str | None = None
    brightness: int | None = None

    @classmethod
    def from_json(cls, raw_payload: str) -> LightCommandPayload:
        """
        Parses a raw JSON string into a LightCommandPayload object.
        Gracefully handles missing keys and invalid JSON, and coerces types.
        """
        try:
            data = json.loads(raw_payload)
            if not isinstance(data, dict):
                return cls()  # Return empty payload if JSON is not a dict
        except json.JSONDecodeError:
            return cls()  # Return empty payload on parsing error

        state = data.get("state")
        if isinstance(state, str):
            state = state.strip().lower()
            if state not in ("on", "off"):
                state = None  # TODO: Log this invalid state
        elif state is not None:
            state = None

        brightness = data.get("brightness")
        if brightness is not None:
            if isinstance(brightness, int | float):
                brightness = get_safe_brightness(brightness)
            elif isinstance(brightness, str):
                try:
                    brightness = get_safe_brightness(brightness)
                except (ValueError, TypeError):
                    brightness = None
            else:
                brightness = None

        return cls(state=state, brightness=brightness)
