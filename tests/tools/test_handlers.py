from requests import Response

from schemas.v1.balance_object import BalanceObject
from schemas.v1.error_response_object import ErrorResponseObject
from schemas.general_objects import UndetectedObject
from tools.handlers import handler_response_api


class ListWrapper:
    def __init__(self, items):
        self.items = items


def test_handler_response_api_wraps_dict():
    result = handler_response_api(
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
    result = handler_response_api(ListWrapper, [1, 2, 3])

    assert isinstance(result, ListWrapper)
    assert result.items == [1, 2, 3]


def test_handler_response_api_returns_response_unchanged():
    response = Response()

    result = handler_response_api(None, response)

    assert result == response


def test_handler_response_api_returns_error_object_on_type_error():
    result = handler_response_api(
        BalanceObject,
        {
            "retval": 1,
            "retdesc": "Bad request",
        },
    )

    assert isinstance(result, ErrorResponseObject)
    assert result.retval == 1
    assert result.retdesc == "Bad request"
