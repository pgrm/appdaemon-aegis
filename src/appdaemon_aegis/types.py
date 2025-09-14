from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Literal


class EntityId(str):
    """
    A strongly-typed Home Assistant entity ID.
    Provides no extra functionality over a string, but improves type checking.
    """
    pass


StateType = Literal["ON", "OFF"]
"""A type for the state of a light device."""


LevelProvider = EntityId | Callable[[], Awaitable[float | None]]
"""
A callback or entity that provides the current physical state of a device.

- If an `EntityId` is provided, the framework will read the state of that entity.
- If a `Callable` is provided, the framework will await the callable, which should
  return a float representing the current power/brightness level, or None if unknown.
"""
