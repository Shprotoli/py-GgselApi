import asyncio
from datetime import datetime

from api.v1.account import Account, AsyncAccount
from parameters.account import CodeFilter, Type


def test_account_helper_builds_balance_route(sync_client):
    api = Account(sync_client)

    assert api._seller_balance_info() == {"route": "sellers/account/balance/info"}


def test_account_helper_builds_receipts_route(sync_client):
    api = Account(sync_client)
    start = datetime(2024, 1, 1, 3, 0, 0)
    finish = datetime(2024, 1, 2, 3, 0, 0)

    payload = api._seller_receipts(
        page=2,
        count=50,
        currency="RUB",
        type=Type.PRODUCT_SALES,
        code_filter=CodeFilter.ONLY_WAITING_CODE_CHECK,
        allow_type=Type.ADD_FUNDS,
        start=start,
        finish=finish,
    )

    assert payload == {
        "route": "sellers/account/receipts",
        "params": {
            "page": 2,
            "count": 50,
            "currency": "RUB",
            "type": Type.PRODUCT_SALES,
            "code_filter": CodeFilter.ONLY_WAITING_CODE_CHECK,
            "allow_type": Type.ADD_FUNDS,
            "start": "2024-01-01T00:00:00",
            "finish": "2024-01-02T00:00:00",
        },
    }


def test_account_sync(sync_client, response_factory):
    balance_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "errors": [],
            "content": {
                "amount_t_lock": 1,
                "amount_t_free": 2,
                "amount_t_plus": 3,
            },
        }
    )
    receipts_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "errors": [],
            "content": {
                "page": 1,
                "count": 2,
                "has_next_page": False,
                "has_previous_page": False,
                "total_count": 2,
                "total_pages": 1,
                "items": [
                    {
                        "account_operation_id": 1,
                        "operation": {
                            "id": 1,
                            "type": "product_sales",
                            "datetime": "2024-01-01T00:00:00",
                            "percent": 10,
                            "price": 100,
                            "currency": "RUB",
                            "on_account": 90,
                        },
                        "owner_id": 7,
                        "product": {"id": 1, "name": [], "deleted": False},
                        "code_check_datetime": "",
                        "date_free": "",
                        "free_description": "",
                        "response": "",
                    }
                ],
            },
        }
    )
    sync_client.get.side_effect = [balance_response, receipts_response]

    api = Account(sync_client)
    balance = api.seller_balance_info()
    receipts = api.seller_receipts(
        page=1,
        count=2,
        currency="RUB",
        type=Type.PRODUCT_SALES,
        code_filter=CodeFilter.HIDE_WAITING_CODE_CHECK,
        allow_type=Type.AGENT_ACCRUALS,
        start="2024-01-01T00:00:00",
        finish="2024-01-02T00:00:00",
    )

    assert balance.content["amount_t_free"] == 2
    assert receipts.content["page"] == 1
    assert receipts.content["items"][0]["owner_id"] == 7

    assert sync_client.get.call_args_list[0].kwargs == {
        "route": "sellers/account/balance/info",
    }
    assert sync_client.get.call_args_list[1].kwargs == {
        "route": "sellers/account/receipts",
        "params": {
            "page": 1,
            "count": 2,
            "currency": "RUB",
            "type": Type.PRODUCT_SALES,
            "code_filter": CodeFilter.HIDE_WAITING_CODE_CHECK,
            "allow_type": Type.AGENT_ACCRUALS,
            "start": "2024-01-01T00:00:00",
            "finish": "2024-01-02T00:00:00",
        },
    }


def test_account_async(async_client, response_factory):
    balance_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "errors": [],
            "content": {
                "amount_t_lock": 1,
                "amount_t_free": 2,
                "amount_t_plus": 3,
            },
        }
    )
    receipts_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "errors": [],
            "content": {
                "page": 1,
                "count": 2,
                "has_next_page": False,
                "has_previous_page": False,
                "total_count": 2,
                "total_pages": 1,
                "items": [
                    {
                        "account_operation_id": 1,
                        "operation": {
                            "id": 1,
                            "type": "product_sales",
                            "datetime": "2024-01-01T00:00:00",
                            "percent": 10,
                            "price": 100,
                            "currency": "RUB",
                            "on_account": 90,
                        },
                        "owner_id": 7,
                        "product": {"id": 1, "name": [], "deleted": False},
                        "code_check_datetime": "",
                        "date_free": "",
                        "free_description": "",
                        "response": "",
                    }
                ],
            },
        }
    )
    async_client.get.side_effect = [balance_response, receipts_response]

    api = AsyncAccount(async_client)
    balance = asyncio.run(api.seller_balance_info())
    receipts = asyncio.run(
        api.seller_receipts(
            page=1,
            count=2,
            currency="RUB",
            type=Type.PRODUCT_SALES,
            code_filter=CodeFilter.HIDE_WAITING_CODE_CHECK,
            allow_type=Type.AGENT_ACCRUALS,
            start="2024-01-01T00:00:00",
            finish="2024-01-02T00:00:00",
        )
    )

    assert balance.content["amount_t_plus"] == 3
    assert receipts.content["count"] == 2
    assert receipts.content["items"][0]["account_operation_id"] == 1

    assert async_client.get.call_args_list[0].kwargs == {
        "route": "sellers/account/balance/info",
    }
    assert async_client.get.call_args_list[1].kwargs == {
        "route": "sellers/account/receipts",
        "params": {
            "page": 1,
            "count": 2,
            "currency": "RUB",
            "type": Type.PRODUCT_SALES,
            "code_filter": CodeFilter.HIDE_WAITING_CODE_CHECK,
            "allow_type": Type.AGENT_ACCRUALS,
            "start": "2024-01-01T00:00:00",
            "finish": "2024-01-02T00:00:00",
        },
    }
