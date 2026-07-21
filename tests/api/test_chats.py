import asyncio
from unittest.mock import AsyncMock
import json

from api.v1.chats import Chats, AsyncChats
from parameters.api import EnumCrudMethod


def test_chats_create_message_helper(sync_client):
    api = Chats(sync_client)

    payload = api._create_message_without_file(777, "hello")

    assert payload["route"] == "debates/v2"
    assert payload["params"] == {"id_i": 777}
    assert json.loads(payload["data"]) == {"message": "hello"}


def test_chats_create_message_without_file_sync(sync_client, response_factory):
    response = response_factory({"status_code": 200})
    sync_client.request.return_value = response

    api = Chats(sync_client)
    result = api.create_message_without_file(777, "hello")

    sync_client.request.assert_called_once_with(
        method=EnumCrudMethod.POST,
        route="debates/v2",
        params={"id_i": 777},
        data=json.dumps({"message": "hello"}),
    )
    assert result == {"status_code": 200}


def test_chats_list_messages_sync(sync_client, response_factory):
    response = response_factory(
        {
            "messages": [
                {
                    "id": 1,
                    "message": "hello",
                    "buyer": 2,
                    "seller": 3,
                    "deleted": 0,
                    "date_written": "2024-01-01T00:00:00",
                    "date_seen": "2024-01-01T00:01:00",
                    "is_file": 0,
                    "filename": "",
                    "url": "",
                    "is_img": 0,
                    "preview": "",
                }
            ]
        }
    )
    sync_client.request.return_value = response

    api = Chats(sync_client)
    result = api.list_messages(777, id_from=1, id_to=9, newer=True, count=150)

    sync_client.request.assert_called_once_with(
        method=EnumCrudMethod.GET,
        route="debates/v2",
        params={
            "id_i": 777,
            "id_from": 1,
            "id_to": 9,
            "newer": 1,
            "count": 100,
        },
    )
    assert result.messages[0]["message"] == "hello"


def test_chats_list_chats_sync(sync_client, response_factory):
    response = response_factory(
        {
            "cnt_pages": 2,
            "items": [
                {
                    "id_i": 1,
                    "email": "buyer@example.com",
                    "product": 100,
                    "last_message": "hello",
                    "cnt_msg": 4,
                    "cnt_new": 1,
                }
            ],
        }
    )
    sync_client.request.return_value = response

    api = Chats(sync_client)
    result = api.list_chats(filter_new=True, email="buyer@example.com", id_ds="ds-1", pagesize=30, page=2)

    sync_client.request.assert_called_once_with(
        method=EnumCrudMethod.GET,
        route="debates/v2/chats",
        params={
            "filter_new": True,
            "email": "buyer@example.com",
            "id_ds": "ds-1",
            "pagesize": 30,
            "page": 2,
        },
    )
    assert result.cnt_pages == 2
    assert result.items[0]["cnt_new"] == 1


def test_chats_async(async_client, response_factory):
    messages_response = response_factory(
        {
            "messages": [
                {
                    "id": 1,
                    "message": "hello",
                    "buyer": 2,
                    "seller": 3,
                    "deleted": 0,
                    "date_written": "2024-01-01T00:00:00",
                    "date_seen": "2024-01-01T00:01:00",
                    "is_file": 0,
                    "filename": "",
                    "url": "",
                    "is_img": 0,
                    "preview": "",
                }
            ]
        }
    )
    chats_response = response_factory(
        {
            "cnt_pages": 2,
            "items": [
                {
                    "id_i": 1,
                    "email": "buyer@example.com",
                    "product": 100,
                    "last_message": "hello",
                    "cnt_msg": 4,
                    "cnt_new": 1,
                }
            ],
        }
    )
    create_response = response_factory({"status_code": 200})
    async_client.request = AsyncMock(
        side_effect=[
            create_response,
            messages_response,
            chats_response,
        ]
    )

    api = AsyncChats(async_client)

    created = asyncio.run(api.create_message_without_file(777, "hello"))
    messages = asyncio.run(api.list_messages(777, id_from=1, id_to=9, newer=True, count=150))
    chats = asyncio.run(api.list_chats(filter_new=True, email="buyer@example.com", id_ds="ds-1", pagesize=30, page=2))

    assert created == {"status_code": 200}
    assert messages.messages[0]["message"] == "hello"
    assert chats.items[0]["email"] == "buyer@example.com"
    assert async_client.request.await_count == 3
