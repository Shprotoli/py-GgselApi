# The only live request that changes something: a message to the chat of the test order.
# It is sent only with `GGSEL_LIVE_SEND_MESSAGE=1`.
import os

import pytest

from ggsel_py.schemas.other.response_object import CompletedResponseObject

pytestmark = pytest.mark.live

# Always this order: the message must not reach a buyer of another order
ORDER_ID = 33455315
DEFAULT_MESSAGE = "Тестовое сообщение py-GGSel API"


def test_create_message_without_file(send_message_enabled, api_v1, describe_result):
    message = os.environ.get("GGSEL_LIVE_MESSAGE") or DEFAULT_MESSAGE

    result = api_v1.chats.create_message_without_file(ORDER_ID, message)

    # On success the API returns 200 without JSON
    assert isinstance(result, CompletedResponseObject), describe_result(result)
    assert result.status_code == 200
