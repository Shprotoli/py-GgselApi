from collections.abc import Callable
from typing import Any, Protocol, TypeAlias, TypeVar, overload, runtime_checkable

from schemas.error_response_object import ErrorResponseObject
from schemas.ggsel_object import GgselGlobalObject

T = TypeVar("T")


@runtime_checkable
class ResponseLike(Protocol):
    def json(self) -> Any: ...


ApiResult: TypeAlias = GgselGlobalObject | ErrorResponseObject | ResponseLike


@overload
def handler_response_api(
    type_wrapper: None,
    data: ResponseLike,
) -> ResponseLike: ...


@overload
def handler_response_api(
    type_wrapper: Callable[..., T],
    data: list[Any],
) -> T: ...


@overload
def handler_response_api(
    type_wrapper: Callable[..., T],
    data: dict[str, Any],
) -> T | ErrorResponseObject: ...


def handler_response_api(
    type_wrapper: Callable[..., T] | None,
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
        if isinstance(data, dict):
            return ErrorResponseObject(**data)
        return data
