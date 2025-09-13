import abc
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Union

from appdaemon.plugins.hass.hassapi import Hass


class AegisApp(Hass, abc.ABC):
    """
    AegisApp, a strongly-typed interface for AppDaemon apps.
    """

    # This is not an exhaustive list of all methods, but it covers some of
    # the most common ones and demonstrates the approach of adding strong types.

    @abc.abstractmethod
    async def initialize(self) -> None:
        """
        This method is called by AppDaemon when the app is initialized.
        It should be implemented by the user's app.
        """
        pass

    # Re-typing methods from Hass for stronger type hints

    async def ping(self) -> Optional[float]:
        return await super().ping()

    async def check_for_entity(
        self, entity_id: str, namespace: Optional[str] = None
    ) -> bool:
        return await super().check_for_entity(entity_id, namespace)

    def get_tracker_details(
        self, person: bool = True, namespace: Optional[str] = None, copy: bool = True
    ) -> Dict[str, Any]:
        return super().get_tracker_details(person, namespace, copy)

    def get_trackers(
        self, person: bool = True, namespace: Optional[str] = None
    ) -> List[str]:
        return super().get_trackers(person, namespace)

    def get_tracker_state(
        self,
        entity_id: str,
        attribute: Optional[str] = None,
        default: Optional[Any] = None,
        namespace: Optional[str] = None,
        copy: bool = True,
    ) -> Any:
        return super().get_tracker_state(entity_id, attribute, default, namespace, copy)

    async def anyone_home(
        self, person: bool = True, namespace: Optional[str] = None
    ) -> bool:
        return await super().anyone_home(person, namespace)

    async def everyone_home(
        self, person: bool = True, namespace: Optional[str] = None
    ) -> bool:
        return await super().everyone_home(person, namespace)

    async def noone_home(
        self, person: bool = True, namespace: Optional[str] = None
    ) -> bool:
        return await super().noone_home(person, namespace)

    async def call_service(
        self,
        service: str,
        namespace: Optional[str] = None,
        timeout: Optional[Union[str, int, float]] = None,
        callback: Optional[Callable[..., Any]] = None,
        hass_timeout: Optional[Union[str, int, float]] = None,
        suppress_log_messages: bool = False,
        **data: Any,
    ) -> Any:
        return await super().call_service(
            service,
            namespace=namespace,
            timeout=timeout,
            callback=callback,
            hass_timeout=hass_timeout,
            suppress_log_messages=suppress_log_messages,
            **data,
        )

    async def turn_on(
        self, entity_id: str, namespace: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        return await super().turn_on(entity_id, namespace=namespace, **kwargs)

    async def turn_off(
        self, entity_id: str, namespace: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        return await super().turn_off(entity_id, namespace=namespace, **kwargs)

    async def toggle(
        self, entity_id: str, namespace: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        return await super().toggle(entity_id, namespace=namespace, **kwargs)

    async def get_history(
        self,
        entity_id: Union[str, List[str]],
        days: Optional[int] = None,
        start_time: Optional[Union[datetime, str]] = None,
        end_time: Optional[Union[datetime, str]] = None,
        minimal_response: Optional[bool] = None,
        no_attributes: Optional[bool] = None,
        significant_changes_only: Optional[bool] = None,
        callback: Optional[Callable[..., Any]] = None,
        namespace: Optional[str] = None,
    ) -> Optional[List[List[Dict[str, Any]]]]:
        return await super().get_history(
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

    async def render_template(
        self, template: str, namespace: Optional[str] = None, **kwargs: Any
    ) -> Any:
        return await super().render_template(template, namespace=namespace, **kwargs)
