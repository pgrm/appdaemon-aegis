# SPDX-FileCopyrightText: 2024-present Jules <jules@example.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import asyncio
from abc import ABC
from collections.abc import Callable, Coroutine, Iterable, Mapping
from datetime import date, datetime, time, timedelta
from logging import Logger
from typing import Any, Literal, TypeVar


class AegisApp(TypedHass, ABC):
    """Base class to intuitively write tested, reliable, and maintainable AppDaemon apps."""
