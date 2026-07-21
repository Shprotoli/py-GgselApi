from unittest.mock import Mock

import pytest

from api.ggsel_api import GgselApiV1, GgselApiV2

# V1
from api.v1.account import Account
from api.v1.api_login import ApiLogin
from api.v1.categories import Categories
from api.v1.chats import Chats
from api.v1.orders import Orders
from api.v1.products import Products
from api.v1.reviews import Reviews

# V2
from api.v2.categories import Categories as CategoriesV2
from api.v2.option import Option as OptionV2


# ==========================================================
# Fixtures
# ==========================================================


@pytest.fixture
def sync_client():
    client = Mock()

    client.params = {
        "token": "OLD_TOKEN",
        "foo": "bar",
    }

    client.token = "OLD_TOKEN"

    client.set_token = Mock()

    return client


# ==========================================================
# V1 API
# ==========================================================


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
def test_v1_lazy_init_all_categories(
        sync_client,
        attribute,
        expected_type,
):
    api = GgselApiV1(
        client=sync_client
    )

    first = getattr(api, attribute)
    second = getattr(api, attribute)

    assert isinstance(first, expected_type)
    assert first is second
    assert first.client is api._client_legacy


def test_v1_creates_two_clients(sync_client):
    api = GgselApiV1(
        client=sync_client
    )

    assert api._client_legacy is sync_client

    assert api._client is not sync_client
    assert api._client_legacy is not api._client


def test_v1_legacy_client_keeps_token(sync_client):
    api = GgselApiV1(
        client=sync_client
    )

    assert api._client_legacy.params["token"] == "OLD_TOKEN"


def test_v1_new_client_removes_token(sync_client):
    api = GgselApiV1(
        client=sync_client
    )

    assert "token" not in api._client.params
    assert api._client.params["foo"] == "bar"


def test_v1_set_token_updates_v2_client(sync_client):
    api = GgselApiV1(
        client=sync_client
    )

    api.client.set_token.reset_mock()

    api.set_token("ABC123")

    api.client.set_token.assert_called_once_with(
        "ABC123"
    )


# ==========================================================
# V2 API
# ==========================================================


@pytest.mark.parametrize(
    ("attribute", "expected_type"),
    [
        ("categories", CategoriesV2),
        ("option", OptionV2),
    ],
)
def test_v2_lazy_init_all_categories(
        sync_client,
        attribute,
        expected_type,
):
    api = GgselApiV2(
        client=sync_client
    )

    first = getattr(api, attribute)
    second = getattr(api, attribute)

    assert isinstance(first, expected_type)
    assert first is second
    assert first.client is api._client


def test_v2_contains_v1_api(sync_client):
    api = GgselApiV2(
        client=sync_client
    )

    assert api.api_v1 is not None
    assert api.api_v1.client_legacy is api._client_legacy


def test_v2_has_separate_clients(sync_client):
    api = GgselApiV2(
        client=sync_client
    )

    assert api._client is not api._client_legacy
    assert api.api_v1.client_legacy is api._client_legacy
    assert api.client is api._client


def test_v2_client_property_returns_v2_client(sync_client):
    api = GgselApiV2(
        client=sync_client
    )

    assert api.client is api._client


def test_v2_client_setter_updates_v2_only(sync_client):
    api = GgselApiV2(
        client=sync_client
    )

    categories = api.categories
    account = api.api_v1.account

    new_client = Mock()
    new_client.params = {}
    new_client.set_token = Mock()

    api.client = new_client

    assert api.client is not new_client
    assert api.client.params == new_client.params
    assert api.client is api._client
    assert categories.client is api._client
    assert account.client is api._client_legacy


def test_v2_set_token_updates_v2_client(sync_client):
    api = GgselApiV2(
        client=sync_client
    )

    api._client.set_token.reset_mock()

    api.set_token("TOKEN")

    api._client.set_token.assert_called_once_with(
        "TOKEN"
    )
