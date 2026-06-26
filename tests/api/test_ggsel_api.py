from unittest.mock import Mock

import pytest

from api.ggsel_api import GgselApiV1, GgselApiV2
from api.v1.account import Account
from api.v1.api_login import ApiLogin
from api.v1.categories import Categories
from api.v1.chats import Chats
from api.v1.orders import Orders
from api.v1.products import Products
from api.v1.reviews import Reviews


@pytest.mark.parametrize(
    ("attribute", "expected_type"),
    [
        ("api_login", ApiLogin),
        ("account", Account),
        ("categories", Categories),
        ("chats", Chats),
        ("products", Products),
        ("orders", Orders),
        ("reviews", Reviews),
    ],
)
def test_v1_lazy_init_all_categories(sync_client, attribute, expected_type):
    api = GgselApiV1(client=sync_client)

    first = getattr(api, attribute)
    second = getattr(api, attribute)

    assert isinstance(first, expected_type)
    assert first is second


def test_v1_client_setter_updates_existing_instances(sync_client):
    new_client = Mock()
    new_client.set_token = Mock()

    api = GgselApiV1(client=sync_client)
    api.api_login
    api.account
    api.categories
    api.chats
    api.products
    api.orders
    api.reviews

    api.client = new_client

    assert api.client is new_client
    assert api.api_login.client is new_client
    assert api.account.client is new_client
    assert api.categories.client is new_client
    assert api.chats.client is new_client
    assert api.products.client is new_client
    assert api.orders.client is new_client
    assert api.reviews.client is new_client


def test_v1_set_token_delegates_to_client(sync_client):
    api = GgselApiV1(client=sync_client)

    api.set_token("ABC123")

    sync_client.set_token.assert_called_with("ABC123")


def test_v2_wraps_v1_and_propagates_client(sync_client):
    new_client = Mock()
    new_client.set_token = Mock()

    api = GgselApiV2(client=sync_client)
    assert api.api_v1.client is sync_client

    _ = api.api_v1.account
    api.client = new_client

    assert api.client is new_client
    assert api.api_v1.client is new_client
    assert api.api_v1.account.client is new_client
