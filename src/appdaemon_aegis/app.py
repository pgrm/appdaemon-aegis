# SPDX-FileCopyrightText: 2024-present Jules <jules@example.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from abc import ABC

from appdaemon.plugins.hass.hassapi import Hass


class AegisApp(Hass, ABC):
    """Base class to intuitively write tested, reliable, and maintainable AppDaemon apps."""
