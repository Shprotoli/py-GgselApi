import asyncio
import json

import httpx
import pytest

from ggsel_py import GgselApiMaster, AsyncGClient, ApiLimiter
from ggsel_py.api.client import LIMIT_ASYNC_REQUESTS, LIMIT_REQUESTS_PER_SECOND


@pytest.fixture
def limiter():
    yield ApiLimiter
    ApiLimiter.configure(LIMIT_ASYNC_REQUESTS, LIMIT_REQUESTS_PER_SECOND)


def make_async_client(requests_log: list[httpx.Request], **kwargs) -> AsyncGClient:
    async def handler(request: httpx.Request) -> httpx.Response:
        requests_log.append(request)
        await asyncio.sleep(0)
        return httpx.Response(200, json={"retval": 0, "cnt_pages": 1, "items": []})

    client = AsyncGClient(**kwargs)
    client._httpx_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return client


def test_master_routes_concurrent_v1_and_v2_requests(limiter):
    requests_log: list[httpx.Request] = []
    client = make_async_client(requests_log, headers={"Authorization": "API-KEY"})
    api = GgselApiMaster(api_key="API-KEY", token="TOKEN", client=client)
    # One slot at a time makes the requests queue behind each other
    limiter.configure(1, 1000)

    async def scenario():
        await asyncio.gather(
            api.api_v1.chats.list_chats(),
            api.api_v2.categories.list_of_categories(parent_id=1),
            api.api_v1.orders.last_sales(),
            api.api_v2.offers.get_offer(id=5),
        )

    asyncio.run(scenario())

    paths = sorted(request.url.path for request in requests_log)
    assert paths == [
        "/api_sellers/api/debates/v2/chats",
        "/api_sellers/api/seller-last-sales",
        "/api_sellers/v2/categories",
        "/api_sellers/v2/offers/5",
    ]

    for request in requests_log:
        assert request.url.host == "seller.ggsel.com"
        if request.url.path.startswith("/api_sellers/api/"):
            assert request.url.params["token"] == "TOKEN"
            assert "authorization" not in request.headers
        else:
            assert "token" not in request.url.params
            assert request.headers["authorization"] == "API-KEY"


def test_async_request_sends_params_headers_and_body(limiter):
    requests_log: list[httpx.Request] = []
    client = make_async_client(requests_log)
    api = GgselApiMaster(token="TOKEN", client=client)

    asyncio.run(api.api_v1.chats.create_message_without_file(id_i=42, message="hi"))

    (request,) = requests_log
    assert request.method == "POST"
    assert str(request.url).startswith("https://seller.ggsel.com/api_sellers/api/debates/v2?")
    assert request.url.params["id_i"] == "42"
    assert request.url.params["token"] == "TOKEN"
    assert request.headers["content-type"] == "application/json"
    assert json.loads(request.content) == {"message": "hi"}


def test_async_client_retries_on_rate_limit(limiter, monkeypatch):
    calls = []

    async def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if len(calls) < 3:
            return httpx.Response(429, json={})
        return httpx.Response(200, json={"retval": 0, "cnt_pages": 1, "items": []})

    async def no_sleep(_):
        return None

    monkeypatch.setattr("ggsel_py.api.client.sleep", no_sleep)
    client = AsyncGClient()
    client._httpx_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    limiter.configure(10, 1000)

    response = asyncio.run(client.get("debates/v2/chats"))

    assert response.status_code == 200
    assert len(calls) == 3
