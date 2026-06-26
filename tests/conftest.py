from unittest.mock import AsyncMock, Mock

import pytest


@pytest.fixture
def response_factory():
    def factory(payload=None):
        response = Mock()
        response.json.return_value = {} if payload is None else payload
        return response

    return factory


@pytest.fixture
def sync_client():
    client = Mock()
    client.get = Mock()
    client.post = Mock()
    client.put = Mock()
    client.set_token = Mock()
    return client


@pytest.fixture
def async_client():
    client = Mock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.put = AsyncMock()
    client.set_token = Mock()
    return client
