import asyncio
from unittest.mock import AsyncMock, patch

from api.client import AsyncGClient, SyncGClient


def test_sync_client_request_merges_headers_and_params():
    client = SyncGClient(
        headers={"Authorization": "API-KEY"},
        params={"token": "TOKEN"},
    )
    response = object()

    with patch("api.client.requests.request", return_value=response) as request_mock:
        result = client.get(
            "categories",
            headers={"lang": "en-US"},
            params={"page": 2},
            data={"hello": "world"},
        )

    assert result is response
    request_mock.assert_called_once_with(
        "get",
        "https://seller.ggsel.com/api_sellers/api/categories",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "API-KEY",
            "lang": "en-US",
        },
        params={
            "token": "TOKEN",
            "page": 2,
        },
        data={"hello": "world"},
        timeout=10,
    )


def test_async_client_request_and_close():
    client = AsyncGClient(
        headers={"Authorization": "API-KEY"},
        params={"token": "TOKEN"},
        timeout=5.0,
    )
    response = object()
    client._httpx_client.request = AsyncMock(return_value=response)
    client._httpx_client.aclose = AsyncMock()

    async def run():
        result = await client.post(
            "products/list",
            headers={"lang": "en-US"},
            params={"page": 2},
            data={"hello": "world"},
        )
        await client.__aexit__(None, None, None)
        return result

    result = asyncio.run(run())

    assert result is response
    client._httpx_client.request.assert_awaited_once_with(
        "POST",
        "products/list",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "API-KEY",
            "lang": "en-US",
        },
        params={
            "token": "TOKEN",
            "page": 2,
        },
        data={"hello": "world"},
    )
    client._httpx_client.aclose.assert_awaited_once()
