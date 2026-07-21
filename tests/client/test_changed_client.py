import pytest

from api.ggsel_api import (
    GgselApi,
    GgselApiV1,
    GgselApiV2,
)
from api.client import SyncGClient, AsyncGClient


class FakeSyncClient(SyncGClient):
    def __init__(self):
        self.params = {}
        self.token = None
        self._base_route = None

    def set_token(self, token):
        self.token = token


class FakeAsyncClient(AsyncGClient):
    def __init__(self):
        self.params = {}
        self.token = None
        self._base_route = None

    def set_token(self, token):
        self.token = token


class FakeV1Sync:
    VERSION_ROUTE = "V1"
    ROUTE = "/api/v1"

    def __init__(self, client):
        self.client = client


class FakeV1Async(FakeV1Sync):
    pass


class FakeV2Sync:
    VERSION_ROUTE = "V2"
    ROUTE = "/api/v2"

    def __init__(self, client):
        self.client = client


class FakeV2Async(FakeV2Sync):
    pass


@pytest.fixture
def patched_objects(monkeypatch):
    objects = {
        "_fake_v1": (FakeV1Sync, FakeV1Async),
        "_fake_v2": (FakeV2Sync, FakeV2Async),
    }

    monkeypatch.setattr(
        "api.ggsel_api.API_OBJECTS",
        objects,
    )

    return objects


@pytest.fixture
def api(patched_objects):
    api = GgselApi()
    api._objects_instance = tuple(patched_objects.keys())

    return api


# -------------------------------------------------------
# client generation
# -------------------------------------------------------


def test_init_generates_two_clients():
    api = GgselApi()

    assert api.client is not api.client_legacy
    assert isinstance(api.client, SyncGClient)
    assert isinstance(api.client_legacy, SyncGClient)


def test_set_client_recreates_clients(api):
    old_client = api.client

    new_client = SyncGClient()

    api.client = new_client

    assert api.client is not old_client
    assert api.client_legacy is new_client
    assert api.client is not new_client


# -------------------------------------------------------
# lazy initialization
# -------------------------------------------------------


def test_get_instance_creates_sync_v1(api):
    api.client = SyncGClient()

    instance = api._get_api_instance("_fake_v1")

    assert isinstance(instance, FakeV1Sync)
    assert instance.client is api.client_legacy


def test_get_instance_creates_sync_v2(api):
    api.client = SyncGClient()

    instance = api._get_api_instance("_fake_v2")

    assert isinstance(instance, FakeV2Sync)
    assert instance.client is api.client


def test_get_instance_is_cached(api):
    first = api._get_api_instance("_fake_v1")
    second = api._get_api_instance("_fake_v1")

    assert first is second


# -------------------------------------------------------
# client update without mode change
# -------------------------------------------------------


def test_update_client_instance_updates_v1_and_v2(api):
    api.client = SyncGClient()

    v1 = api._get_api_instance("_fake_v1")
    v2 = api._get_api_instance("_fake_v2")

    new_client = SyncGClient()

    api.client = new_client

    assert v1.client is api.client_legacy
    assert v2.client is api.client


def test_update_client_instance_sets_routes(api):
    api.client = SyncGClient()

    api._get_api_instance("_fake_v1")
    api._get_api_instance("_fake_v2")

    api._update_client_instance()

    assert api.client_legacy._base_route == "/api/v1"
    assert api.client._base_route == "/api/v2"


# -------------------------------------------------------
# sync / async switching
# -------------------------------------------------------


def test_switch_sync_to_async_recreates_instances(api):
    api.client = FakeSyncClient()

    old = api._get_api_instance("_fake_v1")

    api.client = FakeAsyncClient()

    new = api._get_api_instance("_fake_v1")

    assert old is not new
    assert isinstance(new, FakeV1Async)


def test_switch_async_to_sync_recreates_instances(api):
    api.client = FakeAsyncClient()

    old = api._get_api_instance("_fake_v1")

    api.client = FakeSyncClient()

    new = api._get_api_instance("_fake_v1")

    assert old is not new
    assert isinstance(new, FakeV1Sync)


def test_async_client_keeps_async_instance(api):
    api.client = FakeAsyncClient()

    instance = api._get_api_instance("_fake_v2")

    assert isinstance(instance, FakeV2Async)
    assert instance.client is api.client


# -------------------------------------------------------
# internal methods
# -------------------------------------------------------


def test_update_mode_instance_to_async(api):
    api._client = AsyncGClient()
    api._client_legacy = AsyncGClient()
    api.__async__ = True

    api._update_mode_instance()

    instance = api._get_api_instance("_fake_v1")

    assert isinstance(instance, FakeV1Async)


def test_update_mode_instance_to_sync(api):
    api._client = SyncGClient()
    api._client_legacy = SyncGClient()
    api.__async__ = False

    api._update_mode_instance()

    instance = api._get_api_instance("_fake_v1")

    assert isinstance(instance, FakeV1Sync)


def test_update_client_instance_without_instances(api):
    api._client = SyncGClient()
    api._objects_instance = ()

    api._update_client_instance()

    assert True


# -------------------------------------------------------
# GgselApiV2
# -------------------------------------------------------


def test_api_v2_creates_v1_api():
    api = GgselApiV2()

    assert isinstance(api.api_v1, GgselApiV1)


def test_api_v2_client_change_updates_v1():
    api = GgselApiV2()

    client = SyncGClient()

    api.client = client

    assert api.api_v1.client is not None
    assert api.api_v1.client_legacy is not None
