"""
The public surface that ggsel_flow imports and calls.
If one of these tests fails, ggsel_flow will break too.
"""
import asyncio
import inspect

import httpx

from ggsel_py import GgselApiMaster, AsyncGClient, SyncGClient, ApiLimiter
from ggsel_py.api.client import LIMIT_ASYNC_REQUESTS, LIMIT_REQUESTS_PER_SECOND
from ggsel_py.tools.handlers import ApiResult
from ggsel_py.schemas.v1.chats_object import ChatsObject
from ggsel_py.schemas.v1.messages_object import MessagesObject
from ggsel_py.schemas.v1.info_order_object import InfoOrderObject
from ggsel_py.schemas.v1.unique_code_object import UniqueCodeObject
from ggsel_py.schemas.v1.error_response_object import ErrorResponseObject


def test_limiter_interface():
    assert isinstance(LIMIT_ASYNC_REQUESTS, int)
    assert isinstance(LIMIT_REQUESTS_PER_SECOND, int)

    try:
        ApiLimiter.configure(2, 3)
    finally:
        ApiLimiter.configure(LIMIT_ASYNC_REQUESTS, LIMIT_REQUESTS_PER_SECOND)


def test_master_construction_and_versions():
    client = AsyncGClient(headers={"Authorization": "API-KEY"})
    api = GgselApiMaster(api_key="API-KEY", token="TOKEN", client=client)

    assert api.api_v1.client.params["token"] == "TOKEN"
    assert api.api_v2.client.headers["Authorization"] == "API-KEY"
    assert isinstance(GgselApiMaster(client=SyncGClient()).api_v1.client, SyncGClient)
    assert ApiResult is not None


def test_used_methods_keep_their_signatures():
    api = GgselApiMaster(api_key="API-KEY", token="TOKEN", client=AsyncGClient())
    expected = {
        api.api_v1.chats.list_chats: ["filter_new", "email", "id_ds", "pagesize", "page"],
        api.api_v1.chats.list_messages: ["id_i", "id_from", "id_to", "newer", "count"],
        api.api_v1.chats.create_message_without_file: ["id_i", "message"],
        api.api_v1.orders.last_sales: ["seller_id", "group", "top", "locale"],
        api.api_v1.orders.order_info: ["invoice_id", "locale"],
        api.api_v1.orders.check_unique_code: ["unique_code"],
    }

    for method, params in expected.items():
        assert inspect.iscoroutinefunction(method)
        assert list(inspect.signature(method).parameters) == params


def _run_with_response(coro_factory, payload, status_code=200):
    async def handler(request):
        return httpx.Response(status_code, json=payload)

    client = AsyncGClient()
    client._httpx_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    api = GgselApiMaster(api_key="API-KEY", token="TOKEN", client=client)
    try:
        return asyncio.run(coro_factory(api))
    finally:
        ApiLimiter.configure(LIMIT_ASYNC_REQUESTS, LIMIT_REQUESTS_PER_SECOND)


def test_response_shapes():
    chat = {"id_i": 1, "email": "a@b.c", "product": 2, "last_message": "x", "cnt_msg": 1, "cnt_new": 1}
    result = _run_with_response(lambda api: api.api_v1.chats.list_chats(), {"cnt_pages": 1, "items": [chat]})

    assert isinstance(result, ChatsObject)
    # Nested objects stay plain dicts: ggsel_flow reads them by key
    assert result.items == [chat]


def test_error_response_is_returned_as_object():
    result = _run_with_response(
        lambda api: api.api_v1.orders.order_info(invoice_id=1),
        {"retval": 1, "retdesc": "not found"},
    )

    assert isinstance(result, ErrorResponseObject)
    assert result.retdesc == "not found"


def test_schema_classes_are_importable():
    for schema in (MessagesObject, InfoOrderObject, UniqueCodeObject):
        assert inspect.isclass(schema)
