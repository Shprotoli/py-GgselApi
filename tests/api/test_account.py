import pytest
from unittest.mock import Mock

from api.ggsel_api import GgselApiV1


@pytest.fixture
def mock_client():
    client = Mock()

    response = Mock()
    response.json.return_value = {
        "retval": 0,
        "retdesc": "OK",
        "errors": [],
        "content": {
            "amount_t_lock": 1,
            "amount_t_free": 2,
            "amount_t_plus": 3,
        },
    }

    client.get.return_value = response
    return client


def test_account_balance(mock_client):
    api = GgselApiV1(client=mock_client)

    result = api.account.seller_balance_info()

    mock_client.get.assert_called_once_with(
        "sellers/account/balance/info"
    )

    assert result.retdesc == "OK"
    assert result.content["amount_t_free"] == 2


def test_set_token_calls_client(mock_client):
    api = GgselApiV1(client=mock_client)

    api.set_token("ABC123")

    mock_client.set_token.assert_any_call("ABC123")


def test_multiple_calls_account(mock_client):
    api = GgselApiV1(client=mock_client)

    api.account.seller_balance_info()
    api.account.seller_balance_info()

    assert mock_client.get.call_count == 2
