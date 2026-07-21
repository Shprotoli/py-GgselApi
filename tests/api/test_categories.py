import asyncio
from unittest.mock import AsyncMock

from api.v1.categories import Categories, AsyncCategories
from parameters.api import EnumCrudMethod


def test_categories_helper_builds_route(sync_client):
    api = Categories(sync_client)

    payload = api._all_categories(page=2, count=25, category_id="12", lang="en-US")

    assert payload == {
        "method": EnumCrudMethod.GET,
        "route": "categories",
        "params": {
            "page": 2,
            "count": 25,
            "category_id": "12",
        },
        "headers": {
            "lang": "en-US",
        },
    }


def test_categories_sync(sync_client, response_factory):
    response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "category": [
                {"id": 1, "name": "Games", "sub": [], "cnt": 5},
            ],
        }
    )
    sync_client.request.return_value = response

    api = Categories(sync_client)
    result = api.all_categories(page=2, count=25, category_id="12", lang="en-US")

    sync_client.request.assert_called_once_with(
        method=EnumCrudMethod.GET,
        route="categories",
        params={
            "page": 2,
            "count": 25,
            "category_id": "12",
        },
        headers={"lang": "en-US"},
    )
    assert result.retdesc == "OK"
    assert result.category[0]["name"] == "Games"


def test_categories_async(async_client, response_factory):
    response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "category": [
                {"id": 1, "name": "Games", "sub": [], "cnt": 5},
            ],
        }
    )
    async_client.request = AsyncMock(return_value=response)

    api = AsyncCategories(async_client)
    result = asyncio.run(api.all_categories(page=3, count=10, category_id="", lang="ru-RU"))

    async_client.request.assert_awaited_once_with(
        method=EnumCrudMethod.GET,
        route="categories",
        params={
            "page": 3,
            "count": 10,
            "category_id": "",
        },
        headers={"lang": "ru-RU"},
    )
    assert result.retdesc == "OK"
    assert result.category[0]["cnt"] == 5
