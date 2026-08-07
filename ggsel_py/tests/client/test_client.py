import asyncio
from unittest.mock import AsyncMock, patch

from ggsel_py.api.client import AsyncGClient, SyncGClient


def test_sync_client_request_merges_headers_and_params():
    client = SyncGClient(
        headers={"Authorization": "API-KEY"},
        params={"token": "TOKEN"},
    )
    response = object()

    with patch("ggsel_py.api.client.requests.request", return_value=response) as request_mock:
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
