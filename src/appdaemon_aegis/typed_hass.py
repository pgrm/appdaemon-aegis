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

from appdaemon.adapi import ADAPI
from appdaemon.events import EventCallback
from appdaemon.plugins.hass.hassapi import Hass
from appdaemon.state import StateCallback
from appdaemon.services import ServiceCallback

T = TypeVar("T")


class TypedHass(Hass, ABC):
    """Strongly-typed abstract base class for AppDaemon apps."""

    # HASS API methods
    def ping(self) -> float | None:
        return super().ping()

    def check_for_entity(self, entity_id: str, namespace: str | None = None) -> bool:
        return super().check_for_entity(entity_id, namespace=namespace)

    def get_tracker_details(
        self, person: bool = True, namespace: str | None = None, copy: bool = True
    ) -> dict[str, Any]:
        return super().get_tracker_details(
            person=person, namespace=namespace, copy=copy
        )

    def get_trackers(
        self, person: bool = True, namespace: str | None = None
    ) -> list[str]:
        return super().get_trackers(person=person, namespace=namespace)

    def get_tracker_state(
        self,
        entity_id: str,
        attribute: str | None = None,
        default: Any | None = None,
        namespace: str | None = None,
        copy: bool = True,
    ) -> Any:
        return super().get_tracker_state(
            entity_id,
            attribute=attribute,
            default=default,
            namespace=namespace,
            copy=copy,
        )

    def anyone_home(self, person: bool = True, namespace: str | None = None) -> bool:
        return super().anyone_home(person=person, namespace=namespace)

    def everyone_home(self, person: bool = True, namespace: str | None = None) -> bool:
        return super().everyone_home(person=person, namespace=namespace)

    def noone_home(self, person: bool = True, namespace: str | None = None) -> bool:
        return super().noone_home(person=person, namespace=namespace)

    def constrain_presence(
        self, value: Literal["everyone", "anyone", "noone"] | None = None
    ) -> bool:
        return super().constrain_presence(value)

    def constrain_person(
        self, value: Literal["everyone", "anyone", "noone"] | None = None
    ) -> bool:
        return super().constrain_person(value)

    def constrain_input_boolean(self, value: str | Iterable[str]) -> bool:
        return super().constrain_input_boolean(value)

    def constrain_input_select(self, value: str | Iterable[str]) -> bool:
        return super().constrain_input_select(value)

    def get_service_info(self, service: str) -> dict | None:
        return super().get_service_info(service)

    def turn_on(
        self, entity_id: str, namespace: str | None = None, **kwargs: Any
    ) -> dict:
        return super().turn_on(entity_id, namespace=namespace, **kwargs)

    def turn_off(
        self, entity_id: str, namespace: str | None = None, **kwargs: Any
    ) -> dict:
        return super().turn_off(entity_id, namespace=namespace, **kwargs)

    def toggle(
        self, entity_id: str, namespace: str | None = None, **kwargs: Any
    ) -> dict:
        return super().toggle(entity_id, namespace=namespace, **kwargs)

    def get_history(
        self,
        entity_id: str | list[str],
        days: int | None = None,
        start_time: datetime | str | None = None,
        end_time: datetime | str | None = None,
        minimal_response: bool | None = None,
        no_attributes: bool | None = None,
        significant_changes_only: bool | None = None,
        callback: Callable | None = None,
        namespace: str | None = None,
    ) -> list[list[dict[str, Any]]] | None:
        return super().get_history(
            entity_id=entity_id,
            days=days,
            start_time=start_time,
            end_time=end_time,
            minimal_response=minimal_response,
            no_attributes=no_attributes,
            significant_changes_only=significant_changes_only,
            callback=callback,
            namespace=namespace,
        )

    def get_logbook(
        self,
        entity: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        days: int | None = None,
        callback: Callable | None = None,
        namespace: str | None = None,
    ) -> list[dict[str, str | datetime]] | None:
        return super().get_logbook(
            entity=entity,
            start_time=start_time,
            end_time=end_time,
            days=days,
            callback=callback,
            namespace=namespace,
        )

    def set_value(
        self, entity_id: str, value: int | float, namespace: str | None = None
    ) -> None:
        return super().set_value(entity_id, value, namespace=namespace)

    def set_textvalue(
        self, entity_id: str, value: str, namespace: str | None = None
    ) -> None:
        return super().set_textvalue(entity_id, value, namespace=namespace)

    def select_option(
        self, entity_id: str, option: str, namespace: str | None = None
    ) -> None:
        return super().select_option(entity_id, option, namespace=namespace)

    def last_pressed(self, button_id: str, namespace: str | None = None) -> datetime:
        return super().last_pressed(button_id, namespace=namespace)

    def time_since_last_press(
        self, button_id: str, namespace: str | None = None
    ) -> timedelta:
        return super().time_since_last_press(button_id, namespace=namespace)

    def notify(
        self,
        message: str,
        title: str | None = None,
        name: str | None = None,
        namespace: str | None = None,
        **kwargs: Any,
    ) -> None:
        return super().notify(
            message, title=title, name=name, namespace=namespace, **kwargs
        )

    def get_calendar_events(
        self,
        entity_id: str = "calendar.localcalendar",
        days: int = 1,
        hours: int | None = None,
        minutes: int | None = None,
        namespace: str | None = None,
    ) -> list[dict[str, str | datetime]]:
        return super().get_calendar_events(
            entity_id=entity_id,
            days=days,
            hours=hours,
            minutes=minutes,
            namespace=namespace,
        )

    def run_script(
        self,
        entity_id: str,
        namespace: str | None = None,
        return_immediately: bool = True,
        **kwargs: Any,
    ) -> dict:
        return super().run_script(
            entity_id,
            namespace=namespace,
            return_immediately=return_immediately,
            **kwargs,
        )

    def render_template(
        self, template: str, namespace: str | None = None, **kwargs: Any
    ) -> Any:
        return super().render_template(template, namespace=namespace, **kwargs)

    def device_entities(self, device_id: str) -> list[str]:
        return super().device_entities(device_id)

    def device_attr(self, device_or_entity_id: str, attr_name: str) -> str:
        return super().device_attr(device_or_entity_id, attr_name)

    def is_device_attr(
        self, device_or_entity_id: str, attr_name: str, attr_value: str | int | float
    ) -> bool:
        return super().is_device_attr(device_or_entity_id, attr_name, attr_value)

    def device_id(self, entity_id: str) -> str:
        return super().device_id(entity_id)

    def areas(self) -> list[str]:
        return super().areas()

    def area_id(self, lookup_value: str) -> str:
        return super().area_id(lookup_value)

    def area_name(self, lookup_value: str) -> str:
        return super().area_name(lookup_value)

    def area_entities(self, area_name_or_id: str) -> list[str]:
        return super().area_entities(area_name_or_id)

    def area_devices(self, area_name_or_id: str) -> list[str]:
        return super().area_devices(area_name_or_id)

    def integration_entities(self, integration: str) -> list[str]:
        return super().integration_entities(integration)

    def labels(self, input: str | None = None) -> list[str]:
        return super().labels(input)

    def label_id(self, lookup_value: str) -> str:
        return super().label_id(lookup_value)

    def label_name(self, lookup_value: str) -> str:
        return super().label_name(lookup_value)

    def label_areas(self, label_name_or_id: str) -> list[str]:
        return super().label_areas(label_name_or_id)

    def label_devices(self, label_name_or_id: str) -> list[str]:
        return super().label_devices(label_name_or_id)

    def label_entities(self, label_name_or_id: str) -> list[str]:
        return super().label_entities(label_name_or_id)

    # ADAPI methods
    def get_state(
        self,
        entity_id: str | None = None,
        attribute: str | Literal["all"] | None = None,
        default: Any | None = None,
        namespace: str | None = None,
        copy: bool = True,
        **kwargs: Any,
    ) -> Any | dict[str, Any] | None:
        return super().get_state(
            entity_id,
            attribute=attribute,
            default=default,
            namespace=namespace,
            copy=copy,
            **kwargs,
        )

    def set_state(
        self,
        entity_id: str,
        state: Any | None = None,
        namespace: str | None = None,
        attributes: dict[str, Any] | None = None,
        replace: bool = False,
        check_existence: bool = True,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        return super().set_state(
            entity_id,
            state=state,
            namespace=namespace,
            attributes=attributes,
            replace=replace,
            check_existence=check_existence,
            **kwargs,
        )

    def listen_state(
        self,
        callback: StateCallback,
        entity_id: str | Iterable[str] | None,
        namespace: str | None = None,
        new: str | Callable[[Any], bool] | None = None,
        old: str | Callable[[Any], bool] | None = None,
        duration: str | int | float | timedelta | None = None,
        attribute: str | None = None,
        timeout: str | int | float | timedelta | None = None,
        immediate: bool = False,
        oneshot: bool = False,
        pin: bool | None = None,
        pin_thread: int | None = None,
        **kwargs: Any,
    ) -> str | list[str]:
        return super().listen_state(
            callback,
            entity_id,
            namespace=namespace,
            new=new,
            old=old,
            duration=duration,
            attribute=attribute,
            timeout=timeout,
            immediate=immediate,
            oneshot=oneshot,
            pin=pin,
            pin_thread=pin_thread,
            **kwargs,
        )

    def cancel_listen_state(
        self, handle: str, name: str | None = None, silent: bool = False
    ) -> bool:
        return super().cancel_listen_state(handle, name=name, silent=silent)

    def info_listen_state(
        self, handle: str, name: str | None = None
    ) -> tuple[str, str, Any, dict[str, Any]]:
        return super().info_listen_state(handle, name=name)

    def parse_utc_string(self, utc_string: str) -> float:
        return super().parse_utc_string(utc_string)

    def get_tz_offset(self) -> float:
        return super().get_tz_offset()

    def convert_utc(self, utc: str) -> datetime:
        return super().convert_utc(utc)

    def sun_up(self) -> bool:
        return super().sun_up()

    def sun_down(self) -> bool:
        return super().sun_down()

    def parse_time(
        self,
        time_str: str,
        name: str | None = None,
        aware: bool = False,
        today: bool = False,
        days_offset: int = 0,
    ) -> time:
        return super().parse_time(
            time_str, name=name, aware=aware, today=today, days_offset=days_offset
        )

    def parse_datetime(
        self,
        time_str: str,
        name: str | None = None,
        aware: bool = False,
        today: bool = False,
        days_offset: int = 0,
    ) -> datetime:
        return super().parse_datetime(
            time_str, name=name, aware=aware, today=today, days_offset=days_offset
        )

    def get_now(self, aware: bool = True) -> datetime:
        return super().get_now(aware=aware)

    def get_now_ts(self, aware: bool = False) -> float:
        return super().get_now_ts(aware=aware)

    def now_is_between(
        self, start_time_str: str, end_time_str: str, name: str | None = None
    ) -> bool:
        return super().now_is_between(start_time_str, end_time_str, name=name)

    def sunrise(
        self, aware: bool = False, today: bool = False, days_offset: int = 0
    ) -> datetime:
        return super().sunrise(aware=aware, today=today, days_offset=days_offset)

    def sunset(
        self, aware: bool = False, today: bool = False, days_offset: int = 0
    ) -> datetime:
        return super().sunset(aware=aware, today=today, days_offset=days_offset)

    def time(self) -> time:
        return super().time()

    def datetime(self, aware: bool = False) -> datetime:
        return super().datetime(aware=aware)

    def date(self) -> date:
        return super().date()

    def get_timezone(self) -> str:
        return super().get_timezone()

    def run_at(
        self,
        callback: Callable,
        start: str | time | datetime | None = None,
        random_start: int | None = None,
        random_end: int | None = None,
        pin: bool | None = None,
        pin_thread: int | None = None,
        **kwargs: Any,
    ) -> str:
        return super().run_at(
            callback,
            start,
            random_start=random_start,
            random_end=random_end,
            pin=pin,
            pin_thread=pin_thread,
            **kwargs,
        )

    def run_in(
        self,
        callback: Callable,
        delay: str | int | float | timedelta,
        random_start: int | None = None,
        random_end: int | None = None,
        pin: bool | None = None,
        pin_thread: int | None = None,
        **kwargs: Any,
    ) -> str:
        return super().run_in(
            callback,
            delay,
            random_start=random_start,
            random_end=random_end,
            pin=pin,
            pin_thread=pin_thread,
            **kwargs,
        )

    def run_once(
        self,
        callback: Callable,
        start: str | time | datetime | None = None,
        random_start: int | None = None,
        random_end: int | None = None,
        pin: bool | None = None,
        pin_thread: int | None = None,
        **kwargs: Any,
    ) -> str:
        return super().run_once(
            callback,
            start,
            random_start=random_start,
            random_end=random_end,
            pin=pin,
            pin_thread=pin_thread,
            **kwargs,
        )

    def run_every(
        self,
        callback: Callable,
        start: str | time | datetime | None = None,
        interval: str | int | float | timedelta = 0,
        random_start: int | None = None,
        random_end: int | None = None,
        pin: bool | None = None,
        pin_thread: int | None = None,
        **kwargs: Any,
    ) -> str:
        return super().run_every(
            callback,
            start,
            interval,
            random_start=random_start,
            random_end=random_end,
            pin=pin,
            pin_thread=pin_thread,
            **kwargs,
        )

    def run_daily(
        self,
        callback: Callable,
        start: str | time | datetime | None = None,
        random_start: int | None = None,
        random_end: int | None = None,
        pin: bool | None = None,
        pin_thread: int | None = None,
        **kwargs: Any,
    ) -> str:
        return super().run_daily(
            callback,
            start,
            random_start=random_start,
            random_end=random_end,
            pin=pin,
            pin_thread=pin_thread,
            **kwargs,
        )

    def run_hourly(
        self,
        callback: Callable,
        start: str | time | datetime | None = None,
        random_start: int | None = None,
        random_end: int | None = None,
        pin: bool | None = None,
        pin_thread: int | None = None,
        **kwargs: Any,
    ) -> str:
        return super().run_hourly(
            callback,
            start,
            random_start=random_start,
            random_end=random_end,
            pin=pin,
            pin_thread=pin_thread,
            **kwargs,
        )

    def run_minutely(
        self,
        callback: Callable,
        start: str | time | datetime | None = None,
        random_start: int | None = None,
        random_end: int | None = None,
        pin: bool | None = None,
        pin_thread: int | None = None,
        **kwargs: Any,
    ) -> str:
        return super().run_minutely(
            callback,
            start,
            random_start=random_start,
            random_end=random_end,
            pin=pin,
            pin_thread=pin_thread,
            **kwargs,
        )

    def run_at_sunset(
        self,
        callback: Callable,
        repeat: bool = True,
        offset: int | None = None,
        random_start: int | None = None,
        random_end: int | None = None,
        pin: bool | None = None,
        pin_thread: int | None = None,
        **kwargs: Any,
    ) -> str:
        return super().run_at_sunset(
            callback,
            repeat=repeat,
            offset=offset,
            random_start=random_start,
            random_end=random_end,
            pin=pin,
            pin_thread=pin_thread,
            **kwargs,
        )

    def run_at_sunrise(
        self,
        callback: Callable,
        repeat: bool = True,
        offset: int | None = None,
        random_start: int | None = None,
        random_end: int | None = None,
        pin: bool | None = None,
        pin_thread: int | None = None,
        **kwargs: Any,
    ) -> str:
        return super().run_at_sunrise(
            callback,
            repeat=repeat,
            offset=offset,
            random_start=random_start,
            random_end=random_end,
            pin=pin,
            pin_thread=pin_thread,
            **kwargs,
        )

    def timer_running(self, handle: str) -> bool:
        return super().timer_running(handle)

    def cancel_timer(self, handle: str, silent: bool = False) -> bool:
        return super().cancel_timer(handle, silent=silent)

    def info_timer(self, handle: str) -> tuple[datetime, int, dict[str, Any]] | None:
        return super().info_timer(handle)

    def reset_timer(self, handle: str) -> bool:
        return super().reset_timer(handle)

    def register_service(
        self, service: str, cb: Callable, namespace: str | None = None, **kwargs: Any
    ) -> None:
        return super().register_service(service, cb, namespace=namespace, **kwargs)

    def deregister_service(self, service: str, namespace: str | None = None) -> bool:
        return super().deregister_service(service, namespace=namespace)

    def list_services(self, namespace: str = "global") -> list[dict[str, str]]:
        return super().list_services(namespace=namespace)

    def call_service(
        self,
        service: str,
        namespace: str | None = None,
        timeout: str | int | float | None = None,
        callback: ServiceCallback | None = None,
        hass_timeout: str | int | float | None = None,
        suppress_log_messages: bool = False,
        **data: Any,
    ) -> Any:
        return super().call_service(
            service,
            namespace=namespace,
            timeout=timeout,
            callback=callback,
            hass_timeout=hass_timeout,
            suppress_log_messages=suppress_log_messages,
            **data,
        )

    def run_sequence(
        self,
        sequence: str | list[dict[str, dict[str, str]]],
        namespace: str | None = None,
    ) -> Any:
        return super().run_sequence(sequence, namespace=namespace)

    def cancel_sequence(self, handle: Any) -> None:
        return super().cancel_sequence(handle)

    def listen_event(
        self,
        callback: EventCallback,
        event: str | list[str] | None = None,
        *,
        namespace: str | None = None,
        timeout: str | int | float | timedelta | None = None,
        oneshot: bool = False,
        pin: bool | None = None,
        pin_thread: int | None = None,
        **kwargs: Any | Callable[[Any], bool],
    ) -> str | list[str]:
        return super().listen_event(
            callback,
            event,
            namespace=namespace,
            timeout=timeout,
            oneshot=oneshot,
            pin=pin,
            pin_thread=pin_thread,
            **kwargs,
        )

    def cancel_listen_event(
        self, handle: str | Iterable[str], *, silent: bool = False
    ) -> bool | dict[str, bool]:
        return super().cancel_listen_event(handle, silent=silent)

    def info_listen_event(self, handle: str) -> bool:
        return super().info_listen_event(handle)

    def fire_event(
        self,
        event: str,
        namespace: str | None = None,
        timeout: str | int | float | timedelta | None = -1,
        **kwargs: Any,
    ) -> None:
        return super().fire_event(event, namespace=namespace, timeout=timeout, **kwargs)

    def log(
        self,
        msg: str,
        *args: Any,
        level: str | int = "INFO",
        log: str | None = None,
        ascii_encode: bool | None = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
        **kwargs: Any,
    ) -> None:
        return super().log(
            msg,
            *args,
            level=level,
            log=log,
            ascii_encode=ascii_encode,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
            **kwargs,
        )

    def error(
        self,
        msg: str,
        *args: Any,
        level: str | int = "INFO",
        ascii_encode: bool = True,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
        **kwargs: Any,
    ) -> None:
        return super().error(
            msg,
            *args,
            level=level,
            ascii_encode=ascii_encode,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
            **kwargs,
        )

    def listen_log(
        self,
        callback: Callable,
        level: str | int = "INFO",
        namespace: str = "admin",
        log: str | None = None,
        pin: bool | None = None,
        pin_thread: int | None = None,
        **kwargs: Any,
    ) -> list[str] | None:
        return super().listen_log(
            callback,
            level=level,
            namespace=namespace,
            log=log,
            pin=pin,
            pin_thread=pin_thread,
            **kwargs,
        )

    def cancel_listen_log(self, handle: str) -> None:
        return super().cancel_listen_log(handle)

    def get_main_log(self) -> Logger:
        return super().get_main_log()

    def get_error_log(self) -> Logger:
        return super().get_error_log()

    def get_user_log(self, log: str) -> Logger:
        return super().get_user_log(log)

    def set_log_level(self, level: str | int) -> None:
        return super().set_log_level(level)

    def set_error_level(self, level: str | int) -> None:
        return super().set_error_level(level)

    def get_app(self, name: str) -> ADAPI:
        return super().get_app(name)

    @staticmethod
    def get_ad_version() -> str:
        return ADAPI.get_ad_version()

    def entity_exists(self, entity_id: str, namespace: str | None = None) -> bool:
        return super().entity_exists(entity_id, namespace=namespace)

    def split_entity(self, entity_id: str, namespace: str | None = None) -> list:
        return super().split_entity(entity_id, namespace=namespace)

    def remove_entity(self, entity_id: str, namespace: str | None = None) -> None:
        return super().remove_entity(entity_id, namespace=namespace)

    @staticmethod
    def split_device_list(devices: str) -> list[str]:
        return ADAPI.split_device_list(devices)

    def get_plugin_config(self, namespace: str | None = None) -> Any:
        return super().get_plugin_config(namespace=namespace)

    def friendly_name(self, entity_id: str, namespace: str | None = None) -> str | None:
        return super().friendly_name(entity_id, namespace=namespace)

    def set_production_mode(self, mode: bool = True) -> bool | None:
        return super().set_production_mode(mode)

    def start_app(self, app: str) -> None:
        return super().start_app(app)

    def stop_app(self, app: str) -> None:
        return super().stop_app(app)

    def restart_app(self, app: str) -> None:
        return super().restart_app(app)

    def reload_apps(self) -> None:
        return super().reload_apps()

    def create_task(
        self,
        coro: Coroutine[Any, Any, T],
        callback: Callable | None = None,
        name: str | None = None,
        **kwargs: Any,
    ) -> asyncio.Task[T]:
        return super().create_task(coro, callback=callback, name=name, **kwargs)

    async def run_in_executor(
        self, func: Callable[..., T], *args: Any, **kwargs: Any
    ) -> T:
        return await super().run_in_executor(func, *args, **kwargs)

    @staticmethod
    async def sleep(delay: float, result: Any = None) -> None:
        return await ADAPI.sleep(delay, result=result)
