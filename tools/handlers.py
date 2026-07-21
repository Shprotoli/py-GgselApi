from collections.abc import Callable as CallableABC
from typing import Callable
from typing import Any, Protocol, TypeAlias, TypeVar, overload, runtime_checkable

from requests import Response
from requests.exceptions import JSONDecodeError

from api.client import GClient
from schemas.ggsel_object import GgselObjectApi
from schemas.v1.error_response_object import ErrorResponseObject
from schemas.v2.error_with_entity_object import ErrorWithEntityObject
from schemas.general_objects import UndetectedObject
from schemas.errors.response_object import ResponseJSONErrorObject
from schemas.ggsel_object import GgselGlobalObject

T = TypeVar("T")


@runtime_checkable
class ResponseLike(Protocol):
    def json(self) -> Any: ...


ApiResult: TypeAlias = GgselGlobalObject | ErrorResponseObject | ErrorWithEntityObject | ResponseLike


@overload
def handler_response_api(
        type_wrapper: None,
        data: ResponseLike,
) -> ResponseLike: ...


@overload
def handler_response_api(
        type_wrapper: CallableABC[..., T],
        data: list[Any],
) -> T: ...


@overload
def handler_response_api(
        type_wrapper: CallableABC[..., T],
        data: dict[str, Any],
) -> T | ErrorResponseObject: ...


def handler_response_api(
        type_wrapper: CallableABC[..., T] | None,
        data: ResponseLike | dict[str, Any] | list[Any],
) -> Any:
    """
    Universal API response handler.

    The function accepts already-parsed payloads and maps them into the
    requested domain object when possible.
    """
    if type_wrapper is None:
        return data

    try:
        match data:
            case list():
                return type_wrapper(data)
            case dict():
                return type_wrapper(**data)
            case _ if isinstance(data, ResponseLike):
                return data
            case _:
                return data
    except TypeError:
        version_api = "V1" if not hasattr(type_wrapper, "VERSION_API") else getattr(type_wrapper, "VERSION_API")

        try:
            match version_api:
                case "V1":
                    if isinstance(data, dict):
                        return ErrorResponseObject(**data)
                case "V2":
                    if isinstance(data, dict):
                        return ErrorWithEntityObject(**data)
        except TypeError:
            return UndetectedObject(data=data)
        return UndetectedObject(data=data)


def handler_response(response: Response):
    try:
        data = response.json()
    except JSONDecodeError:
        return ResponseJSONErrorObject(
            status_code=response.status_code,
            text=response.text,
            headers=dict(response.headers),
            url=response.url,
            method=response.request.method if response.request else None
        )
    return data


def handler_api(
        client: GClient,
        func_api: Callable[..., dict],
        schedule_object: GgselObjectApi,
        **params,
) -> ApiResult:
    """
    This function makes a request to the API using the passed client
    and passes the response to the API response handler - "handler_response_api", after which it returns the result

    Example Code:
    async_handler_api(self.client, self._search_categories, ListOfCategories, page=page, limit=limit, q=q, locale=locale)

    :param client: The client for making requests
    :param func_api: A class method that inherits from `Category`
    :param schedule_object: API Response Object
    :param params: Arguments required by the `func_api` method
    :return:
    """
    response = client.request(**func_api(**params))
    data = handler_response(response)

    return handler_response_api(schedule_object, data=data)


async def async_handler_api(
        client: GClient,
        func_api: Callable[..., dict],
        schedule_object: GgselObjectApi,
        **params,
) -> ApiResult:
    """
    This function makes a async request to the API using the passed client
    and passes the response to the API response handler - "handler_response_api", after which it returns the result

    Example Code:
    async_handler_api(self.client, self._search_categories, ListOfCategories, page=page, limit=limit, q=q, locale=locale)

    :param client: The client for making requests
    :param func_api: A class method that inherits from `Category`
    :param schedule_object: API Response Object
    :param params: Arguments required by the `func_api` method
    :return:
    """
    response = await client.request(**func_api(**params))
    data = handler_response(response)

    return handler_response_api(schedule_object, data=data)
