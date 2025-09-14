from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class LightCommandPayload:
    """A structured representation of a command payload for a light device."""
    state: str | None = None
    brightness: int | None = None

    @classmethod
    def from_json(cls, raw_payload: str) -> LightCommandPayload:
        """
        Parses a raw JSON string into a LightCommandPayload object.
        Gracefully handles missing keys and invalid JSON.
        """
        try:
            data = json.loads(raw_payload)
            if not isinstance(data, dict):
                return cls() # Return empty payload if JSON is not a dict
        except json.JSONDecodeError:
            return cls() # Return empty payload on parsing error

        state = data.get("state")
        brightness = data.get("brightness")

        # Basic type validation
        if state is not None and not isinstance(state, str):
            state = None
        if brightness is not None and not isinstance(brightness, int):
            brightness = None

        return cls(state=state, brightness=brightness)
