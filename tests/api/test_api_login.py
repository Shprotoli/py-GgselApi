import asyncio
from unittest.mock import AsyncMock
import json

from api.v1.api_login import ApiLogin, AsyncApiLogin


def test_api_login_helper_builds_json_payload(sync_client):
    api = ApiLogin(sync_client)

    payload = api._api_login(42, 1234567890, "sign-value")

    assert payload["route"] == "apilogin"
    assert json.loads(payload["data"]) == {
        "seller_id": 42,
        "timestamp": "1234567890",
        "sign": "sign-value",
    }


def test_api_login_sync(sync_client, response_factory):
    response = response_factory(
        {
            "retval": 0,
            "desc": "OK",
            "token": "TOKEN-123",
            "seller_id": 42,
            "valid_thru": "2030-01-01T00:00:00",
        }
    )
    sync_client.request.return_value = response

    api = ApiLogin(sync_client)
    result = api.api_login(42, 1234567890, "sign-value")

    sync_client.request.assert_called_once()
    call_kwargs = sync_client.request.call_args.kwargs
    assert call_kwargs["route"] == "apilogin"
    assert json.loads(call_kwargs["data"]) == {
        "seller_id": 42,
        "timestamp": "1234567890",
        "sign": "sign-value",
    }
    assert result.token == "TOKEN-123"
    assert result.seller_id == 42


def test_api_login_async(async_client, response_factory):
    response = response_factory(
        {
            "retval": 0,
            "desc": "OK",
            "token": "TOKEN-ASYNC",
            "seller_id": 99,
            "valid_thru": "2030-01-01T00:00:00",
        }
    )
    async_client.request = AsyncMock(return_value=response)

    api = AsyncApiLogin(async_client)
    result = asyncio.run(api.api_login(99, "1234567890", "sign-value"))

    async_client.request.assert_awaited_once()
    call_kwargs = async_client.request.call_args.kwargs
    assert call_kwargs["route"] == "apilogin"
    assert json.loads(call_kwargs["data"]) == {
        "seller_id": 99,
        "timestamp": "1234567890",
        "sign": "sign-value",
    }
    assert result.token == "TOKEN-ASYNC"
    assert result.seller_id == 99
