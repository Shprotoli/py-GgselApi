from collections.abc import Callable as CallableABC
from typing import Callable
from typing import Any, Protocol, TypeAlias, TypeVar, overload, runtime_checkable

from requests import Response
from json import JSONDecodeError

from api.client import GClient
from schemas.ggsel_object import GgselObjectApi
from schemas.v1.error_response_object import ErrorResponseObject
from schemas.v2.error_with_entity_object import ErrorWithEntityObject
from schemas.general_objects import UndetectedObject
from schemas.other.response_object import (
    JSONErrorResponseObject,
    CompletedResponseObject,
    UnknownResponseObject,
    ResponseApiResult,
    ErrorsResponseObject,
)
from schemas.ggsel_object import GgselGlobalObject

T = TypeVar("T")


@runtime_checkable
class ResponseLike(Protocol):
    def json(self) -> Any: ...


ApiResult: TypeAlias = GgselGlobalObject | ErrorResponseObject | ErrorWithEntityObject | ResponseLike
ErrorApiResult: TypeAlias = ErrorResponseObject | ErrorWithEntityObject | UndetectedObject


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


class ToolHandlerResponse:
    @classmethod
    def return_type_wrapper_is_none(
            cls,
            data: dict[str, Any] | list[Any],
    ):
        """
        The method for handling cases when the type_wrapper argument (a type from the schemas folder) is None.
        """
        match data:
            case {"other": _}:
                return ErrorWithEntityObject(**data)
            case _:
                return UndetectedObject(data=data)

    @classmethod
    def return_error(
            cls,
            type_wrapper: CallableABC[..., T] | None,
            data: dict[str, Any] | list[Any],
    ) -> ErrorApiResult:
        version_api = "V1" if not hasattr(type_wrapper, "VERSION_API") else getattr(type_wrapper, "VERSION_API")

        try:
            match version_api:
                case "V1" if isinstance(data, dict):
                    return ErrorResponseObject(**data)
                case "V2" if isinstance(data, dict):
                    return ErrorWithEntityObject(**data)
                case _:
                    return UndetectedObject(data=data)
        except TypeError:
            return UndetectedObject(data=data)

    @classmethod
    def return_by_data(
            cls,
            type_wrapper: CallableABC[..., T] | None,
            data: dict[str, Any] | list[Any],
    ):
        match data:
            case list():
                return type_wrapper(data)
            case dict():
                return type_wrapper(**data)
            case _:
                return UndetectedObject(data=data)


def handler_response_api(
        type_wrapper: CallableABC[..., T] | None,
        data: dict[str, Any],
) -> Any:
    """
    Universal API response handler.

    The function accepts already-parsed payloads and maps them into the
    requested domain object when possible.
    """
    if not isinstance(data, dict) and not isinstance(data, list):
        """
        If `data` comes as an object that is not a `dict`/`list` type (it is expected to be a `dict` (or `list` type)
        because earlier in the code, in the `handler_response` function, we get it from the JSON response of our `Response` object),
        then `data` is already an object that can be returned.
        """
        return data

    if type_wrapper is None:
        return ToolHandlerResponse.return_type_wrapper_is_none(data)

    try:
        return ToolHandlerResponse.return_by_data(type_wrapper, data)
    except TypeError:
        return ToolHandlerResponse.return_error(type_wrapper, data)


def handler_response(response: Response | ResponseLike) -> ResponseApiResult | dict[str, Any] | list[Any]:
    try:
        data = response.json()
    except JSONDecodeError:
        response_data = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "url": response.url,
            "method": response.request.method if response.request else None,
        }

        match response.status_code:
            case 401:
                return JSONErrorResponseObject(
                    text=response.text,
                    **response_data
                )

            case status if 400 <= status < 500:
                return ErrorsResponseObject(
                    text=response.text,
                    **response_data
                )

            case status if 200 <= status < 300:
                return CompletedResponseObject(
                    **response_data
                )

            case _:
                return UnknownResponseObject(
                    **response_data
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

    return handler_response_api(type_wrapper=schedule_object, data=data)


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

    return handler_response_api(type_wrapper=schedule_object, data=data)
