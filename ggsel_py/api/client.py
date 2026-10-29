from abc import ABC
from http import HTTPStatus
from typing import Any
from asyncio import Semaphore, sleep

from aiolimiter import AsyncLimiter
from httpx import Response as AsyncResponse, AsyncClient
import requests
from requests import Response

from ggsel_py.parameters.api import EnumCrudMethod, TOKEN_PARAM

LIMIT_ASYNC_REQUESTS = 15
LIMIT_REQUESTS_PER_SECOND = 15

# Responses after which the request is repeated
STATUS_CODE_ERROR = (HTTPStatus.SERVICE_UNAVAILABLE, HTTPStatus.TOO_MANY_REQUESTS)


class ApiLimiter:
    _semaphore = Semaphore(LIMIT_ASYNC_REQUESTS)
    _limiter = AsyncLimiter(LIMIT_REQUESTS_PER_SECOND, 1)

    @classmethod
    def configure(
            cls,
            limit_async_requests: int = LIMIT_ASYNC_REQUESTS,
            limit_requests_per_second: int = LIMIT_REQUESTS_PER_SECOND
    ):
        cls._semaphore = Semaphore(limit_async_requests)
        cls._limiter = AsyncLimiter(limit_requests_per_second, 1)

    @classmethod
    async def run(cls, coro_factory, retries=3):
        result = None

        for attempt in range(retries):
            async with cls._semaphore:
                async with cls._limiter:
                    result = await coro_factory()

            if result.status_code not in STATUS_CODE_ERROR:
                return result

            # The pause happens outside the semaphore so that it does not hold a slot of other requests
            await sleep(attempt)

        return result


class GClient(ABC):
    def __init__(
            self,
            protocol: str,
            domain: str,
            base_route: str,
            **kwargs,
    ):
        self.protocol = protocol.lower()
        self.domain = domain
        self._base_route = base_route

        self.headers: dict[str, Any] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            **kwargs.pop("headers", {})
        }
        self.params: dict[str, Any] = {**kwargs.pop("params", {})}

    def set_token(self, token: str) -> None:
        self.params[TOKEN_PARAM] = token

    @property
    def base_url(self) -> str:
        return f"{self.protocol}://{self.domain}/{self._base_route}"

    def build_url(self, route: str) -> str:
        return f"{self.base_url}/{route}"

    def _build_headers(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        return {**self.headers, **kwargs.pop("headers", {})}

    def _build_params(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        return {**self.params, **kwargs.pop("params", {})}


class SyncGClient(GClient):
    def __init__(
            self,
            protocol: str = "https",
            domain: str = "seller.ggsel.com",
            base_route: str = "api_sellers/api",
            timeout: float = 10,
            **kwargs,
    ):
        super().__init__(protocol, domain, base_route, **kwargs)
        self.timeout = timeout

    def request(self, route: str, method: str, **kwargs: Any) -> Response:
        return requests.request(
            method,
            self.build_url(route),
            headers=self._build_headers(kwargs),
            params=self._build_params(kwargs),
            data=kwargs.get("data"),
            timeout=self.timeout,
        )

    def get(self, route: str, **kwargs: Any) -> Response:
        return self.request(route, EnumCrudMethod.GET, **kwargs)

    def post(self, route: str, **kwargs: Any) -> Response:
        return self.request(route, EnumCrudMethod.POST, **kwargs)

    def put(self, route: str, **kwargs: Any) -> Response:
        return self.request(route, EnumCrudMethod.PUT, **kwargs)


class AsyncGClient(GClient):
    def __init__(
            self,
            protocol: str = "https",
            domain: str = "seller.ggsel.com",
            base_route: str = "api_sellers/api",
            timeout: float = 15.0,

            limit_async_requests: int = 10,
            limit_requests_per_second: int = 5,
            **kwargs,
    ):
        super().__init__(protocol, domain, base_route, **kwargs)

        ApiLimiter.configure(limit_async_requests, limit_requests_per_second)
        # The connection pool may be shared by copies of this client (see `GgselApiMaster`),
        # so the URL and headers are passed with each request instead of being stored in the pool
        self._httpx_client = AsyncClient(timeout=timeout)

    async def request(self, route: str, method: str, **kwargs: Any) -> AsyncResponse:
        # Everything is calculated once: `_build_*` consume `kwargs`, and retries must send the same request
        url = self.build_url(route)
        headers = self._build_headers(kwargs)
        params = self._build_params(kwargs)
        data = kwargs.get("data")

        return await ApiLimiter.run(
            lambda: self._httpx_client.request(
                method,
                url,
                headers=headers,
                params=params,
                data=data,
            )
        )

    async def get(self, route: str, **kwargs: Any) -> AsyncResponse:
        return await self.request(route, EnumCrudMethod.GET, **kwargs)

    async def post(self, route: str, **kwargs: Any) -> AsyncResponse:
        return await self.request(route, EnumCrudMethod.POST, **kwargs)

    async def put(self, route: str, **kwargs: Any) -> AsyncResponse:
        return await self.request(route, EnumCrudMethod.PUT, **kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._httpx_client.aclose()
