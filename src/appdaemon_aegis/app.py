# SPDX-FileCopyrightText: 2024-present Jules <jules@example.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from abc import ABC

from .typed_hass import TypedHass


class AegisApp(TypedHass, ABC):
    """Base class to intuitively write tested, reliable, and maintainable AppDaemon apps."""
