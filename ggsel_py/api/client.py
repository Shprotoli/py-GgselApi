from abc import ABC
from typing import Any
from asyncio import Semaphore, sleep

from aiolimiter import AsyncLimiter
from httpx import Response as AsyncResponse, AsyncClient
import requests
from requests import Response

LIMIT_ASYNC_REQUESTS = 15
LIMIT_REQUESTS_PER_SECOND = 15

STATUS_CODE_ERROR = (503, 429)


class ApiLimiter:
    _semaphore = Semaphore(LIMIT_ASYNC_REQUESTS)
    _limiter = AsyncLimiter(LIMIT_REQUESTS_PER_SECOND, 1)

    @classmethod
    def configure(
            cls,
            limit_async_requests: int = LIMIT_ASYNC_REQUESTS,
            limit_requests_per_second: int = LIMIT_ASYNC_REQUESTS
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
        self.params["token"] = token

    @property
    def base_url(self) -> str:
        return f"{self.protocol}://{self.domain}/{self._base_route}"

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
            **kwargs,
    ):
        super().__init__(protocol, domain, base_route, **kwargs)

    def request(self, route: str, method: str, **kwargs: Any) -> Response:
        print(self.base_url, route, self._build_headers(kwargs))
        return requests.request(
            method,
            f"{self.base_url}/{route}",
            headers=self._build_headers(kwargs),
            params=self._build_params(kwargs),
            data=kwargs.get("data"),
            timeout=10,
        )

    def get(self, route: str, **kwargs: Any) -> Response:
        return self.request(route, "get", **kwargs)

    def post(self, route: str, **kwargs: Any) -> Response:
        return self.request(route, "post", **kwargs)

    def put(self, route: str, **kwargs: Any) -> Response:
        return self.request(route, "put", **kwargs)


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
        self._httpx_client = AsyncClient(
            headers=self.headers,
            timeout=timeout,
        )

    async def request(self, route: str, method: str, **kwargs: Any) -> AsyncResponse:
        self._httpx_client.base_url = self.base_url

        return await ApiLimiter.run(
            lambda: self._httpx_client.request(
                method,
                route,
                headers=self._build_headers(kwargs),
                params=self._build_params(kwargs),
                data=kwargs.get("data"),
            )
        )

    async def get(self, route: str, **kwargs: Any) -> AsyncResponse:
        return await self.request(route, "GET", **kwargs)

    async def post(self, route: str, **kwargs: Any) -> AsyncResponse:
        return await self.request(route, "POST", **kwargs)

    async def put(self, route: str, **kwargs: Any) -> AsyncResponse:
        return await self.request(route, "PUT", **kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._httpx_client.aclose()
