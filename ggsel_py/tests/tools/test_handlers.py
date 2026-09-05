from requests import Response

from ggsel_py.schemas.v1.balance_object import BalanceObject
from ggsel_py.schemas.v1.error_response_object import ErrorResponseObject
from ggsel_py.tools.handlers import parse_api_payload


class ListWrapper:
    def __init__(self, items):
        self.items = items


def test_handler_response_api_wraps_dict():
    result = parse_api_payload(
        BalanceObject,
        {
            "retval": 0,
            "retdesc": "OK",
            "errors": [],
            "content": {
                "amount_t_lock": 1,
                "amount_t_free": 2,
                "amount_t_plus": 3,
            },
        },
    )

    assert isinstance(result, BalanceObject)
    assert result.content["amount_t_free"] == 2


def test_handler_response_api_wraps_list():
    result = parse_api_payload(ListWrapper, [1, 2, 3])

    assert isinstance(result, ListWrapper)
    assert result.items == [1, 2, 3]


def test_handler_response_api_returns_response_unchanged():
    response = Response()

    result = parse_api_payload(None, response)

    assert result == response


def test_handler_response_api_returns_error_object_on_type_error():
    result = parse_api_payload(
        BalanceObject,
        {
            "retval": 1,
            "retdesc": "Bad request",
        },
    )

    assert isinstance(result, ErrorResponseObject)
    assert result.retval == 1
    assert result.retdesc == "Bad request"
