from collections.abc import Callable as CallableABC
from typing import Callable, Any, TypeAlias, TypeVar, overload

from http import HTTPStatus
from json import JSONDecodeError

from requests import Response

from ggsel_py.api.client import GClient
from ggsel_py.parameters.api import ApiVersion
from ggsel_py.schemas.ggsel_object import GgselObjectApi
from ggsel_py.schemas.v1.error_response_object import ErrorResponseObject
from ggsel_py.schemas.v2.error_with_entity_object import ErrorWithEntityObject
from ggsel_py.schemas.general_objects import UndetectedObject
from ggsel_py.schemas.other.response_object import (
    JSONErrorResponseObject,
    CompletedResponseObject,
    UnknownResponseObject,
    ResponseApiResult,
    ErrorsResponseObject,
    ResponseLike,
)
from ggsel_py.schemas.ggsel_object import GgselGlobalObject

T = TypeVar("T")

ApiResult: TypeAlias = GgselGlobalObject | ErrorResponseObject | ErrorWithEntityObject
ErrorApiResult: TypeAlias = ErrorResponseObject | ErrorWithEntityObject | UndetectedObject


@overload
def parse_api_payload(
        type_wrapper: None,
        data: ResponseLike,
) -> ResponseLike: ...


@overload
def parse_api_payload(
        type_wrapper: CallableABC[..., T],
        data: list[Any],
) -> T: ...


@overload
def parse_api_payload(
        type_wrapper: CallableABC[..., T],
        data: dict[str, Any],
) -> T | ErrorResponseObject: ...


class ToolHandlerResponse:
    @classmethod
    def handle_untyped_payload(
            cls,
            data: dict[str, Any] | list[Any],
    ) -> ErrorWithEntityObject | UndetectedObject:
        """
        The method for handling cases when the type_wrapper argument (a type from the schemas folder) is None.
        """
        match data:
            case {"other": _}:
                return ErrorWithEntityObject(**data)
            case _:
                return UndetectedObject(data=data)

    @classmethod
    def parse_error_response(
            cls,
            type_wrapper: CallableABC[..., T] | None,
            data: dict[str, Any] | list[Any],
    ) -> ErrorApiResult:
        version_api = getattr(type_wrapper, "VERSION_API", ApiVersion.V1)

        try:
            match version_api:
                case ApiVersion.V1 if isinstance(data, dict):
                    return ErrorResponseObject(**data)
                case ApiVersion.V2 if isinstance(data, dict):
                    return ErrorWithEntityObject(**data)
                case _:
                    return UndetectedObject(data=data)
        except TypeError:
            return UndetectedObject(data=data)

    @classmethod
    def build_response_object(
            cls,
            type_wrapper: CallableABC[..., T],
            data: dict[str, Any] | list[Any],
    ) -> T:
        """Raises `TypeError` when the payload does not match the schema"""
        match data:
            case list():
                return type_wrapper(data)
            case dict():
                return type_wrapper(**data)


def parse_api_payload(
        type_wrapper: CallableABC[..., T] | None,
        data: dict[str, Any],
) -> Any:
    """
    Universal API response handler.

    The function accepts already-parsed payloads and maps them into the
    requested domain object when possible.
    """
    if not isinstance(data, (dict, list)):
        # `parse_http_response` has already turned a non-JSON response into a result object
        return data

    if type_wrapper is None:
        return ToolHandlerResponse.handle_untyped_payload(data)

    try:
        return ToolHandlerResponse.build_response_object(type_wrapper, data)
    except TypeError:
        return ToolHandlerResponse.parse_error_response(type_wrapper, data)


def parse_http_response(response: Response | ResponseLike) -> ResponseApiResult | dict[str, Any] | list[Any]:
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
            case HTTPStatus.UNAUTHORIZED:
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


def request_and_parse(
        client: GClient,
        func_api: Callable[..., dict],
        schedule_object: GgselObjectApi | None,
        **params: Any,
) -> ApiResult:
    """
    This function makes a request to the API using the passed client
    and passes the response to the API response handler - "parse_api_payload", after which it returns the result

    Example Code:
    request_and_parse(self.client, self._search_categories, ListOfCategories, page=page, limit=limit, q=q, locale=locale)

    :param client: The client for making requests
    :param func_api: A class method that inherits from `Category`
    :param schedule_object: API Response Object
    :param params: Arguments required by the `func_api` method
    :return:
    """
    response = client.request(**func_api(**params))
    data = parse_http_response(response)

    return parse_api_payload(type_wrapper=schedule_object, data=data)


async def async_request_and_parse(
        client: GClient,
        func_api: Callable[..., dict],
        schedule_object: GgselObjectApi | None,
        **params: Any,
) -> ApiResult:
    """
    This function makes a async request to the API using the passed client
    and passes the response to the API response handler - "parse_api_payload", after which it returns the result

    Example Code:
    async_request_and_parse(self.client, self._search_categories, ListOfCategories, page=page, limit=limit, q=q, locale=locale)

    :param client: The client for making requests
    :param func_api: A class method that inherits from `Category`
    :param schedule_object: API Response Object
    :param params: Arguments required by the `func_api` method
    :return:
    """
    response = await client.request(**func_api(**params))
    data = parse_http_response(response)

    return parse_api_payload(type_wrapper=schedule_object, data=data)
