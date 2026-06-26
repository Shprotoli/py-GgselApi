import asyncio
import json

from api.v1.products import Products, AsyncProducts
from parameters.products import OrderCol, OrderDir


def test_products_list_helper_handles_scalar_and_sequence(sync_client):
    api = Products(sync_client)

    scalar_payload = api._products_list(15, page=2, count=3, lang="en-US", locale="ru-RU")
    list_payload = api._products_list([1, "2"], page=4, count=5, lang="en-US", locale="ru-RU")

    assert scalar_payload == {
        "route": "products/list",
        "params": {
            "ids": "15",
            "page": 2,
            "count": 3,
        },
        "headers": {
            "lang": "en-US",
            "locale": "ru-RU",
        },
    }
    assert list_payload["params"]["ids"] == "1,2"


def test_products_sync(sync_client, response_factory):
    list_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "page": 1,
            "count": 10,
            "has_next_page": False,
            "has_previous_page": False,
            "total_count": 1,
            "total_pages": 1,
            "rows": [
                {
                    "id_goods": 1,
                    "name_goods": "Product 1",
                }
            ],
        }
    )
    info_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "product": {
                "id": 1,
                "name": "Product 1",
            },
        }
    )
    seller_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "id_seller": 99,
            "name_seller": "Seller",
            "cnt_goods": 2,
            "pages": 1,
            "page": 1,
            "order_col": "order_col",
            "order_dir": "asc",
            "rows": [
                {
                    "id_goods": 1,
                    "name_goods": "Product 1",
                }
            ],
        }
    )

    sync_client.get.side_effect = [list_response, info_response]
    sync_client.post.return_value = seller_response

    api = Products(sync_client)
    product_list = api.products_list([1, 2], page=1, count=10, lang="en-US", locale="ru-RU")
    product_info = api.product_info("product-1")
    seller_goods = api.products_seller(
        99,
        order_col=OrderCol.ORDER_COL,
        order_dir=OrderDir.ASC,
        rows=50,
        page=2,
        currency="RUB",
        lang="en-US",
        show_hidden=True,
        owner_id=7,
    )

    assert product_list.rows[0]["name_goods"] == "Product 1"
    assert product_info.product["name"] == "Product 1"
    assert seller_goods.id_seller == 99
    assert seller_goods.rows[0]["name_goods"] == "Product 1"

    assert sync_client.get.call_args_list[0].kwargs == {
        "route": "products/list",
        "params": {"ids": "1,2", "page": 1, "count": 10},
        "headers": {"lang": "en-US", "locale": "ru-RU"},
    }
    assert sync_client.get.call_args_list[1].kwargs == {
        "route": "products/product-1/data",
    }

    seller_kwargs = sync_client.post.call_args.kwargs
    assert seller_kwargs["route"] == "seller-goods"
    assert json.loads(seller_kwargs["data"]) == {
        "id_seller": 99,
        "order_col": "order_col",
        "order_dir": "asc",
        "rows": 50,
        "page": 2,
        "currency": "RUB",
        "lang": "en-US",
        "show_hidden": True,
        "owner_id": 7,
    }


def test_products_async(async_client, response_factory):
    list_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "page": 1,
            "count": 10,
            "has_next_page": False,
            "has_previous_page": False,
            "total_count": 1,
            "total_pages": 1,
            "rows": [
                {
                    "id_goods": 1,
                    "name_goods": "Product 1",
                }
            ],
        }
    )
    info_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "product": {
                "id": 1,
                "name": "Product 1",
            },
        }
    )
    seller_response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "id_seller": 99,
            "name_seller": "Seller",
            "cnt_goods": 2,
            "pages": 1,
            "page": 1,
            "order_col": "order_col",
            "order_dir": "asc",
            "rows": [
                {
                    "id_goods": 1,
                    "name_goods": "Product 1",
                }
            ],
        }
    )

    async_client.get.side_effect = [list_response, info_response]
    async_client.post.return_value = seller_response

    api = AsyncProducts(async_client)
    product_list = asyncio.run(api.products_list([1, 2], page=1, count=10, lang="en-US", locale="ru-RU"))
    product_info = asyncio.run(api.product_info("product-1"))
    seller_goods = asyncio.run(
        api.products_seller(
            99,
            order_col=OrderCol.ORDER_COL,
            order_dir=OrderDir.ASC,
            rows=50,
            page=2,
            currency="RUB",
            lang="en-US",
            show_hidden=True,
            owner_id=7,
        )
    )

    assert product_list.rows[0]["name_goods"] == "Product 1"
    assert product_info.product["name"] == "Product 1"
    assert seller_goods.id_seller == 99
    assert seller_goods.rows[0]["name_goods"] == "Product 1"

    assert async_client.get.call_args_list[0].kwargs == {
        "route": "products/list",
        "params": {"ids": "1,2", "page": 1, "count": 10},
        "headers": {"lang": "en-US", "locale": "ru-RU"},
    }
    assert async_client.get.call_args_list[1].kwargs == {
        "route": "products/product-1/data",
    }

    seller_kwargs = async_client.post.call_args.kwargs
    assert seller_kwargs["route"] == "seller-goods"
    assert json.loads(seller_kwargs["data"]) == {
        "id_seller": 99,
        "order_col": "order_col",
        "order_dir": "asc",
        "rows": 50,
        "page": 2,
        "currency": "RUB",
        "lang": "en-US",
        "show_hidden": True,
        "owner_id": 7,
    }
