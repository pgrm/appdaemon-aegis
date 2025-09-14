from __future__ import annotations

from typing import List, Optional, Union


class StepDimmedLamp:
    """Represents the logic for a step-dimmable lamp."""

    def __init__(
        self,
        steps: List[Union[float, int]] = [0.25, 0.5, 1.0],
        max_brightness: int = 255,
    ):
        if not steps:
            raise ValueError("Steps cannot be empty.")

        self.max_brightness = max_brightness
        self.brightness_levels = self._normalize_steps(steps)
        self.brightness_to_level_map = {
            brightness: i for i, brightness in enumerate(self.brightness_levels)
        }

    def _normalize_steps(self, steps: List[Union[float, int]]) -> List[int]:
        """Normalize steps to integer brightness values."""
        normalized_steps = []
        for step in steps:
            if isinstance(step, float):
                if not 0.0 <= step <= 1.0:
                    raise ValueError("Float steps must be between 0.0 and 1.0.")
                normalized_steps.append(int(step * self.max_brightness))
            elif isinstance(step, int):
                if not 0 <= step <= self.max_brightness:
                    raise ValueError(
                        f"Integer steps must be between 0 and {self.max_brightness}."
                    )
                normalized_steps.append(step)
            else:
                raise TypeError("Steps must be a list of floats or ints.")
        return sorted(normalized_steps)

    def get_level_from_brightness(self, brightness: int) -> int:
        """Convert a 0-255 brightness value to a level index."""
        if brightness <= 0:
            return -1  # Off

        # Find the closest brightness level
        closest_level = -1
        min_diff = float("inf")

        for i, level_brightness in enumerate(self.brightness_levels):
            diff = abs(brightness - level_brightness)
            if diff < min_diff:
                min_diff = diff
                closest_level = i
        return closest_level

    def get_flicks(self, current_level_index: Optional[int], target_level_index: int) -> int:
        """Calculate the number of flicks to get from current to target level."""
        if not (0 <= target_level_index < len(self.brightness_levels)):
            raise ValueError("Invalid target_level_index.")

        num_levels = len(self.brightness_levels)

        if current_level_index is None or current_level_index == -1:  # Lamp is off
            return target_level_index + 1

        if not (0 <= current_level_index < num_levels):
            raise ValueError("Invalid current_level_index.")

        return (target_level_index - current_level_index + num_levels) % num_levels
