import asyncio
from unittest.mock import AsyncMock

from api.v1.orders import Orders, AsyncOrders
from parameters.api import EnumCrudMethod


def test_orders_last_sales_helper(sync_client):
    api = Orders(sync_client)

    payload = api._last_sales(123, group=False, top=5, locale="en-US")

    assert payload == {
        "method": EnumCrudMethod.GET,
        "route": "seller-last-sales",
        "params": {
            "seller_id": 123,
            "group": False,
            "top": 5,
        },
        "headers": {
            "locale": "en-US",
        },
    }


def test_orders_sync(sync_client, response_factory):
    last_sales_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "sales": [
                {
                    "invoice_id": 1,
                    "date": "2024-01-01T00:00:00",
                    "product": {"id": 10, "name": "Game"},
                }
            ],
        }
    )
    order_info_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "content": {
                "item_id": 1,
                "content_id": 2,
                "cart_uid": "cart-1",
                "name": "Order",
                "amount": 100,
                "currency_type": "RUB",
                "invoice_state": 1,
                "purchase_date": "2024-01-01T00:00:00",
                "date_pay": "2024-01-01T00:00:00",
                "agent_id": 1,
                "agent_percent": 10,
                "agent_fee": 5,
                "query_string": "",
                "unit_goods": "",
                "cnt_goods": "1",
                "promo_code": "",
                "bonus_code": "",
                "feedback": {
                    "deleted": False,
                    "feedback": "",
                    "feedback_type": "",
                    "comment": "",
                },
                "unique_code_state": {
                    "state": 1,
                    "date_check": "2024-01-01T00:00:00",
                    "date_delivery": "2024-01-01T00:00:00",
                    "date_confirmed": "2024-01-01T00:00:00",
                    "date_refuted": "2024-01-01T00:00:00",
                },
                "options": [],
                "buyer_info": {
                    "payment_method": "card",
                    "account": "acc",
                    "email": "buyer@example.com",
                    "phone": "",
                    "skype": "",
                    "whatsapp": "",
                    "ip_address": "",
                    "payment_aggregator": "",
                },
                "owner": 1,
                "day_lock": 0,
                "lock_state": "",
                "profit": 95,
                "external_order_id": "",
            },
        }
    )
    unique_code_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "inv": 11,
            "id_goods": 22,
            "amount": 100,
            "type_curr": "RUB",
            "amount_usd": 2,
            "profit": 95,
            "date_pay": "2024-01-01T00:00:00",
            "email": "buyer@example.com",
            "name_invoice": "Invoice",
            "lang": "ru-RU",
            "agent_id": 1,
            "agent_percent": "10",
            "query_string": "",
            "unit_goods": "",
            "cnt_goods": "1",
            "promo_code": "",
            "bonus_code": "",
            "cart_uid": "cart-1",
            "unique_code_state": {
                "state": 1,
                "date_check": "2024-01-01T00:00:00",
                "date_delivery": "2024-01-01T00:00:00",
                "date_confirmed": "2024-01-01T00:00:00",
                "date_refuted": "2024-01-01T00:00:00",
            },
            "options": [],
        }
    )

    sync_client.request.side_effect = [last_sales_response, order_info_response, unique_code_response]

    api = Orders(sync_client)
    last_sales = api.last_sales(123, group=False, top=5, locale="en-US")
    order_info = api.order_info(555, locale="en-US")
    unique_code = api.check_unique_code("UC-1")

    assert last_sales.sales[0]["product"]["name"] == "Game"
    assert order_info.content["buyer_info"]["email"] == "buyer@example.com"
    assert unique_code.inv == 11

    assert sync_client.request.call_args_list[0].kwargs == {
        "method": EnumCrudMethod.GET,
        "route": "seller-last-sales",
        "params": {"seller_id": 123, "group": False, "top": 5},
        "headers": {"locale": "en-US"},
    }
    assert sync_client.request.call_args_list[1].kwargs == {
        "method": EnumCrudMethod.GET,
        "route": "purchase/info/555",
        "headers": {"locale": "en-US"},
    }
    assert sync_client.request.call_args_list[2].kwargs == {
        "method": EnumCrudMethod.GET,
        "route": "purchases/unique-code/UC-1",
    }


def test_orders_async(async_client, response_factory):
    last_sales_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "sales": [
                {
                    "invoice_id": 1,
                    "date": "2024-01-01T00:00:00",
                    "product": {"id": 10, "name": "Game"},
                }
            ],
        }
    )
    order_info_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "content": {
                "item_id": 1,
                "content_id": 2,
                "cart_uid": "cart-1",
                "name": "Order",
                "amount": 100,
                "currency_type": "RUB",
                "invoice_state": 1,
                "purchase_date": "2024-01-01T00:00:00",
                "date_pay": "2024-01-01T00:00:00",
                "agent_id": 1,
                "agent_percent": 10,
                "agent_fee": 5,
                "query_string": "",
                "unit_goods": "",
                "cnt_goods": "1",
                "promo_code": "",
                "bonus_code": "",
                "feedback": {
                    "deleted": False,
                    "feedback": "",
                    "feedback_type": "",
                    "comment": "",
                },
                "unique_code_state": {
                    "state": 1,
                    "date_check": "2024-01-01T00:00:00",
                    "date_delivery": "2024-01-01T00:00:00",
                    "date_confirmed": "2024-01-01T00:00:00",
                    "date_refuted": "2024-01-01T00:00:00",
                },
                "options": [],
                "buyer_info": {
                    "payment_method": "card",
                    "account": "acc",
                    "email": "buyer@example.com",
                    "phone": "",
                    "skype": "",
                    "whatsapp": "",
                    "ip_address": "",
                    "payment_aggregator": "",
                },
                "owner": 1,
                "day_lock": 0,
                "lock_state": "",
                "profit": 95,
                "external_order_id": "",
            },
        }
    )
    unique_code_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "inv": 11,
            "id_goods": 22,
            "amount": 100,
            "type_curr": "RUB",
            "amount_usd": 2,
            "profit": 95,
            "date_pay": "2024-01-01T00:00:00",
            "email": "buyer@example.com",
            "name_invoice": "Invoice",
            "lang": "ru-RU",
            "agent_id": 1,
            "agent_percent": "10",
            "query_string": "",
            "unit_goods": "",
            "cnt_goods": "1",
            "promo_code": "",
            "bonus_code": "",
            "cart_uid": "cart-1",
            "unique_code_state": {
                "state": 1,
                "date_check": "2024-01-01T00:00:00",
                "date_delivery": "2024-01-01T00:00:00",
                "date_confirmed": "2024-01-01T00:00:00",
                "date_refuted": "2024-01-01T00:00:00",
            },
            "options": [],
        }
    )

    async_client.request = AsyncMock(side_effect=[last_sales_response, order_info_response, unique_code_response])

    api = AsyncOrders(async_client)
    last_sales = asyncio.run(api.last_sales(123, group=False, top=5, locale="en-US"))
    order_info = asyncio.run(api.order_info(555, locale="en-US"))
    unique_code = asyncio.run(api.check_unique_code("UC-1"))

    assert last_sales.sales[0]["product"]["name"] == "Game"
    assert order_info.content["buyer_info"]["email"] == "buyer@example.com"
    assert unique_code.inv == 11

    assert async_client.request.call_args_list[0].kwargs == {
        "method": EnumCrudMethod.GET,
        "route": "seller-last-sales",
        "params": {"seller_id": 123, "group": False, "top": 5},
        "headers": {"locale": "en-US"},
    }
    assert async_client.request.call_args_list[1].kwargs == {
        "method": EnumCrudMethod.GET,
        "route": "purchase/info/555",
        "headers": {"locale": "en-US"},
    }
    assert async_client.request.call_args_list[2].kwargs == {
        "method": EnumCrudMethod.GET,
        "route": "purchases/unique-code/UC-1",
    }
