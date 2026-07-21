import asyncio
from unittest.mock import AsyncMock

from api.v1.reviews import Reviews, AsyncReviews
from parameters.api import EnumCrudMethod


def test_reviews_helper(sync_client):
    api = Reviews(sync_client)

    payload = api._user_reviews(777, type="good", page=3, count=5, locale="en-US")

    assert payload == {
        "method": EnumCrudMethod.GET,
        "route": "reviews",
        "params": {
            "product_id": 777,
            "page": 3,
            "count": 5,
            "type": "good",
        },
        "headers": {
            "locale": "en-US",
        },
    }


def test_reviews_sync(sync_client, response_factory):
    response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "totalPages": 1,
            "totalItems": 1,
            "totalGood": 1,
            "totalBad": 0,
            "reviews": [
                {
                    "id": 1,
                    "info": "Great",
                    "good": 1,
                    "type": "good",
                    "date": "2024-01-01T00:00:00",
                    "invoice_id": 11,
                    "name": "Buyer",
                    "comment": "Nice",
                    "owner_id": 9,
                }
            ],
        }
    )
    sync_client.request.return_value = response

    api = Reviews(sync_client)
    result = api.user_reviews(777, type="good", page=3, count=5, locale="en-US")

    sync_client.request.assert_called_once_with(
        method=EnumCrudMethod.GET,
        route="reviews",
        params={
            "product_id": 777,
            "page": 3,
            "count": 5,
            "type": "good",
        },
        headers={"locale": "en-US"},
    )
    assert result.totalGood == 1
    assert result.reviews[0]["info"] == "Great"


def test_reviews_async(async_client, response_factory):
    response = response_factory(
        {
            "retval": 0,
            "retdesc": "OK",
            "totalPages": 1,
            "totalItems": 1,
            "totalGood": 1,
            "totalBad": 0,
            "reviews": [
                {
                    "id": 1,
                    "info": "Great",
                    "good": 1,
                    "type": "good",
                    "date": "2024-01-01T00:00:00",
                    "invoice_id": 11,
                    "name": "Buyer",
                    "comment": "Nice",
                    "owner_id": 9,
                }
            ],
        }
    )
    async_client.request = AsyncMock(return_value=response)

    api = AsyncReviews(async_client)
    result = asyncio.run(api.user_reviews(777, type="good", page=3, count=5, locale="en-US"))

    async_client.request.assert_awaited_once_with(
        method=EnumCrudMethod.GET,
        route="reviews",
        params={
            "product_id": 777,
            "page": 3,
            "count": 5,
            "type": "good",
        },
        headers={"locale": "en-US"},
    )
    assert result.totalBad == 0
    assert result.reviews[0]["name"] == "Buyer"
