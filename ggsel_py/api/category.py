from __future__ import annotations

import inspect
from abc import ABC
from json import dumps
from typing import (
    Any,
    Callable,
    ClassVar,
    Concatenate,
    Coroutine,
    Generic,
    ParamSpec,
    TypeAlias,
    TypedDict,
    overload,
)

from ggsel_py.api.client import SyncGClient, AsyncGClient
from ggsel_py.parameters.api import ApiVersion, EnumCrudMethod, Header
from ggsel_py.tools.handlers import request_and_parse, async_request_and_parse

GClientType: TypeAlias = SyncGClient | AsyncGClient

P = ParamSpec("P")


class RequestSpec(TypedDict, total=False):
    """Keyword arguments for `GClient.request`, built by an endpoint"""
    method: EnumCrudMethod
    route: str
    params: dict[str, Any]
    headers: dict[str, str]
    data: str


def build_request(
        method: EnumCrudMethod,
        route: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        payload: Any = None,
) -> RequestSpec:
    """
    Builds the arguments of `GClient.request`.
    Parts that were not passed are left out of the result, and `payload` is serialized to JSON.
    """
    request: RequestSpec = {
        "method": method,
        "route": route,
    }
    if params is not None:
        request["params"] = params
    if headers is not None:
        request["headers"] = headers
    if payload is not None:
        request["data"] = dumps(payload)

    return request


def locale_header(locale: Any) -> dict[str, str]:
    return {Header.LOCALE: str(locale)}


class Route(ABC):
    ROUTE: str


class RouteApiV1:
    VERSION_ROUTE: ClassVar[ApiVersion] = ApiVersion.V1
    ROUTE: ClassVar[str] = "api_sellers/api"


class RouteApiV2:
    VERSION_ROUTE: ClassVar[ApiVersion] = ApiVersion.V2
    ROUTE: ClassVar[str] = "api_sellers/v2"


class Category(ABC):
    """
    This class serves as a parent for API category classes (for example: `api_login`).
    Endpoints of a category are called synchronously; see `AsyncCategory` for the asynchronous version.
    """

    def __init__(self, client: GClientType):
        self.client = client

    def _bind_endpoint(self, endpoint: Endpoint[P]) -> Callable[P, Any]:
        def call(*args: P.args, **kwargs: P.kwargs) -> Any:
            return request_and_parse(
                self.client,
                lambda: endpoint.build(self, *args, **kwargs),
                endpoint.schema,
            )

        return endpoint.decorate(call)


class AsyncCategory(Category):
    """The same as `Category`, but endpoints return coroutines"""

    def _bind_endpoint(self, endpoint: Endpoint[P]) -> Callable[P, Coroutine[Any, Any, Any]]:
        async def call(*args: P.args, **kwargs: P.kwargs) -> Any:
            return await async_request_and_parse(
                self.client,
                lambda: endpoint.build(self, *args, **kwargs),
                endpoint.schema,
            )

        return endpoint.decorate(call)


class Endpoint(Generic[P]):
    """
    One API method, described once and shared by the synchronous and asynchronous category classes.

    The decorated function only builds the request (`RequestSpec`); the response is parsed into `schema`.
    Accessed through a `Category` instance, the endpoint is a regular method that returns the parsed result,
    and through an `AsyncCategory` instance — a coroutine function. The public signature and the docstring
    are taken from the decorated function.
    """

    def __init__(
            self,
            builder: Callable[Concatenate[Any, P], RequestSpec],
            schema: Any,
    ):
        self._builder = builder
        self.schema = schema
        self.__name__ = builder.__name__
        self.__doc__ = builder.__doc__

        signature = inspect.signature(builder)
        self.__signature__ = signature.replace(
            parameters=list(signature.parameters.values())[1:],
            return_annotation="ApiResult",
        )

    def build(self, category: Category, *args: P.args, **kwargs: P.kwargs) -> RequestSpec:
        return self._builder(category, *args, **kwargs)

    def decorate(self, call: Callable[..., Any]) -> Callable[..., Any]:
        call.__name__ = self.__name__
        call.__qualname__ = self._builder.__qualname__
        call.__doc__ = self.__doc__
        call.__signature__ = self.__signature__
        return call

    @overload
    def __get__(self, instance: None, owner: type) -> Endpoint[P]: ...

    @overload
    def __get__(self, instance: AsyncCategory, owner: type) -> Callable[P, Coroutine[Any, Any, Any]]: ...

    @overload
    def __get__(self, instance: Category, owner: type) -> Callable[P, Any]: ...

    def __get__(self, instance: Category | None, owner: type) -> Any:
        if instance is None:
            return self
        return instance._bind_endpoint(self)


def endpoint(schema: Any) -> Callable[[Callable[Concatenate[Any, P], RequestSpec]], Endpoint[P]]:
    """
    Turns a request builder into an API method whose response is parsed into `schema`
    (`None` — the response is returned without a specific schema)
    """

    def decorator(builder: Callable[Concatenate[Any, P], RequestSpec]) -> Endpoint[P]:
        return Endpoint(builder, schema)

    return decorator
