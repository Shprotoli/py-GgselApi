import pytest
from unittest.mock import Mock

from api.ggsel_api import GgselApi
from api.client import SyncGClient, AsyncGClient


# -------------------------------------------------------
# Fake objects
# -------------------------------------------------------

class SyncCategory:
    def __init__(self, client):
        self.client = client


class SyncCategoryV1(SyncCategory):
    ROUTE = "/api/v1"


class SyncCategoryV2(SyncCategory):
    ROUTE = "/api/v2"


class AsyncCategory:
    def __init__(self, client):
        self.client = client


class AsyncCategoryV1(AsyncCategory):
    ROUTE = "/api/v1"


@pytest.fixture
def patched_api_objects(monkeypatch):
    mapping = {
        "_test_instance": (SyncCategory, AsyncCategory),
    }

    monkeypatch.setattr("api.ggsel_api.API_OBJECTS", mapping)

    return mapping


@pytest.fixture
def api(patched_api_objects):
    api = GgselApi()
    api._objects_instance = ("_test_instance",)
    return api


def test_change_sync_client_to_sync(api):
    first_client = SyncGClient()
    second_client = SyncGClient()

    api.client = first_client

    instance = api._get_api_instance("_test_instance")

    api.client = second_client

    assert api.client is second_client
    assert instance.client is second_client


def test_change_sync_client_to_async(api):
    sync_client = SyncGClient()
    async_client = AsyncGClient()

    api.client = sync_client

    old_instance = api._get_api_instance("_test_instance")

    api.client = async_client

    new_instance = api._get_api_instance("_test_instance")

    assert isinstance(new_instance, AsyncCategory)
    assert new_instance.client is async_client
    assert old_instance is not new_instance


def test_change_async_client_to_sync(api):
    async_client = AsyncGClient()
    sync_client = SyncGClient()

    api.client = async_client

    old_instance = api._get_api_instance("_test_instance")

    api.client = sync_client

    new_instance = api._get_api_instance("_test_instance")

    assert isinstance(new_instance, SyncCategory)
    assert new_instance.client is sync_client
    assert old_instance is not new_instance


def test_change_async_client_to_async(api):
    first = AsyncGClient()
    second = AsyncGClient()

    api.client = first

    instance = api._get_api_instance("_test_instance")

    api.client = second

    assert instance.client is second


def test_update_client_instance(api):
    client = SyncGClient()

    obj = Mock()
    obj.ROUTE = "/route"

    api._test_instance = obj
    api._client = client

    api._update_client_instance()

    assert obj.client is client
    assert client._base_route == "/route"


def test_update_client_instance_without_instances(api):
    api._client = SyncGClient()

    api._update_client_instance()

    assert not hasattr(api, "_test_instance")


def test_update_client_instance_without_route(api):
    client = SyncGClient()

    obj = Mock(spec=["client"])

    api._client = client
    api._test_instance = obj

    api._update_client_instance()

    assert obj.client is client


def test_update_mode_instance_to_sync(api):
    client = SyncGClient()

    api._client = client
    api.__async__ = False

    api._update_mode_instance()

    assert isinstance(api._get_api_instance("_test_instance"), SyncCategory)
    assert api._get_api_instance("_test_instance").client is client


def test_update_mode_instance_to_async(api):
    client = AsyncGClient()

    api._client = client
    api.__async__ = True

    api._update_mode_instance()

    assert isinstance(api._get_api_instance("_test_instance"), AsyncCategory)
    assert api._get_api_instance("_test_instance").client is client


def test_client_setter_calls_update_client_instance(api, monkeypatch):
    api._client = SyncGClient()
    api.__async__ = False

    update_client = Mock()
    update_mode = Mock()

    monkeypatch.setattr(api, "_update_client_instance", update_client)
    monkeypatch.setattr(api, "_update_mode_instance", update_mode)

    api.client = SyncGClient()

    update_client.assert_called_once()
    update_mode.assert_not_called()


def test_client_setter_calls_update_mode_instance(api, monkeypatch):
    api._client = SyncGClient()
    api.__async__ = False

    update_client = Mock()
    update_mode = Mock()

    monkeypatch.setattr(api, "_update_client_instance", update_client)
    monkeypatch.setattr(api, "_update_mode_instance", update_mode)

    api.client = AsyncGClient()

    update_mode.assert_called_once()
    update_client.assert_not_called()


def test_get_api_instance_sync(api):
    api.client = SyncGClient()

    obj = api._get_api_instance("_test_instance")

    assert isinstance(obj, SyncCategory)
    assert obj.client is api.client


def test_get_api_instance_async(api):
    api.client = AsyncGClient()

    obj = api._get_api_instance("_test_instance")

    assert isinstance(obj, AsyncCategory)
    assert obj.client is api.client


def test_get_api_instance_cached(api):
    api.client = SyncGClient()

    first = api._get_api_instance("_test_instance")
    second = api._get_api_instance("_test_instance")

    assert first is second


def test_get_api_instance_after_sync_to_sync(api):
    first_client = SyncGClient()
    second_client = SyncGClient()

    api.client = first_client

    first = api._get_api_instance("_test_instance")

    api.client = second_client

    second = api._get_api_instance("_test_instance")

    assert first is second
    assert second.client is second_client


def test_get_api_instance_after_sync_to_async(api):
    api.client = SyncGClient()

    first = api._get_api_instance("_test_instance")

    api.client = AsyncGClient()

    second = api._get_api_instance("_test_instance")

    assert first is not second
    assert isinstance(second, AsyncCategory)
    assert second.client is api.client


def test_get_api_instance_after_async_to_sync(api):
    api.client = AsyncGClient()

    first = api._get_api_instance("_test_instance")

    api.client = SyncGClient()

    second = api._get_api_instance("_test_instance")

    assert first is not second
    assert isinstance(second, SyncCategory)
    assert second.client is api.client


def test_get_api_instance_after_async_to_async(api):
    first_client = AsyncGClient()
    second_client = AsyncGClient()

    api.client = first_client

    first = api._get_api_instance("_test_instance")

    api.client = second_client

    second = api._get_api_instance("_test_instance")

    assert first is second
    assert second.client is second_client
