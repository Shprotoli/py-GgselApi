import pytest
from unittest.mock import Mock

from api.ggsel_api import GgselApiV1


@pytest.fixture
def mock_client():
    client = Mock()

    response = Mock()
    client.get.return_value = response
    return client


def test_account_lazy_init(mock_client):
    api = GgselApiV1(client=mock_client)

    a1 = api.account
    a2 = api.account

    assert a1 is a2


def test_api_login_lazy_init(mock_client):
    api = GgselApiV1(client=mock_client)

    a1 = api.api_login
    a2 = api.api_login

    assert a1 is a2


def test_client_setter_updates_dependencies(mock_client):
    new_client = Mock()

    api = GgselApiV1(client=mock_client)

    _ = api.account
    _ = api.api_login

    api.client = new_client

    assert api.client is new_client
    assert api.account.client is new_client
    assert api.api_login.client is new_client
