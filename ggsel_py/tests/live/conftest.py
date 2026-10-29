# Live tests: real requests to the GGSel API.
#
# They run only with `-m live` and only when the credentials are set in `.env.test` (see `.env.test.example`)
# or in the environment. The test that sends a message to the order chat also needs `GGSEL_LIVE_SEND_MESSAGE=1`.
import asyncio
import os
from hashlib import sha256
from pathlib import Path
from time import sleep, time

import pytest

from ggsel_py import AsyncGClient, GgselApiMaster, SyncGClient
from ggsel_py.api.ggsel_api import GgselApiV1, GgselApiV2
from ggsel_py.schemas.ggsel_object import GgselObject
from ggsel_py.schemas.other.response_object import UnknownResponseObject
from ggsel_py.schemas.v1.token_object import TokenObject

ENV_FILE = Path(__file__).resolve().parents[3] / ".env.test"

# V1 `categories` answers in about 20 seconds
TIMEOUT = 60
# Pause after each test: requests one right after another get 429 Too Many Requests
PAUSE_BETWEEN_TESTS = 1


def load_env_file(path: Path) -> None:
    """Puts `KEY=value` lines of `path` into `os.environ`; variables that are already set win"""
    if not path.is_file():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


load_env_file(ENV_FILE)


def env(name: str) -> str:
    return os.environ.get(name, "").strip()


def pytest_configure(config):
    config.addinivalue_line("markers", "live: real requests to the GGSel API (run with -m live)")


def pytest_collection_modifyitems(config, items):
    if "live" in (config.option.markexpr or ""):
        return

    skip = pytest.mark.skip(reason="live test: run with -m live")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip)


def describe(result) -> str:
    # The URL and the headers of a raw response are left out: the URL contains the token
    if isinstance(result, UnknownResponseObject):
        return f"{type(result).__name__}: HTTP {result.status_code} {getattr(result, 'text', '')[:500]}"
    return f"{type(result).__name__}: {result!r:.1500}"


def check_result(result, schema):
    """Checks that the response was parsed into `schema` (and not into an error object)"""
    # `pytest.fail` instead of `assert`: pytest would print the repr of the response, and its URL contains the token
    if not isinstance(result, schema):
        pytest.fail(f"expected {schema.__name__}, got {describe(result)}")
    if isinstance(result, GgselObject) and result.retval != 0:
        pytest.fail(f"retval={result.retval}: {describe(result)}")
    return result


@pytest.fixture(scope="session")
def expect():
    return check_result


@pytest.fixture(scope="session")
def describe_result():
    return describe


@pytest.fixture(autouse=True)
def pause_between_tests():
    yield
    sleep(PAUSE_BETWEEN_TESTS)


@pytest.fixture(scope="session")
def api_key() -> str:
    key = env("GGSEL_API_KEY")
    if not key:
        pytest.skip("GGSEL_API_KEY is not set (.env.test)")
    return key


@pytest.fixture(scope="session")
def token() -> str:
    """The V1 token: `GGSEL_TOKEN`, or one received by `api_login` from `GGSEL_SELLER_ID` + `GGSEL_API_SECRET`"""
    if env("GGSEL_TOKEN"):
        return env("GGSEL_TOKEN")

    seller_id, secret = env("GGSEL_SELLER_ID"), env("GGSEL_API_SECRET")
    if not (seller_id and secret):
        pytest.skip("neither GGSEL_TOKEN nor GGSEL_SELLER_ID + GGSEL_API_SECRET are set (.env.test)")

    timestamp = str(int(time() * 1000))
    sign = sha256((secret + timestamp).encode()).hexdigest()
    result = GgselApiV1().api_login.api_login(int(seller_id), timestamp, sign)

    return check_result(result, TokenObject).token


@pytest.fixture(scope="session")
def seller_id() -> int:
    if not env("GGSEL_SELLER_ID"):
        pytest.skip("GGSEL_SELLER_ID is not set (.env.test)")
    return int(env("GGSEL_SELLER_ID"))


@pytest.fixture(scope="session")
def unique_code() -> str:
    if not env("GGSEL_LIVE_UNIQUE_CODE"):
        pytest.skip("GGSEL_LIVE_UNIQUE_CODE is not set (.env.test)")
    return env("GGSEL_LIVE_UNIQUE_CODE")


@pytest.fixture(scope="session")
def send_message_enabled() -> None:
    if env("GGSEL_LIVE_SEND_MESSAGE") != "1":
        pytest.skip("sending a real message is off: set GGSEL_LIVE_SEND_MESSAGE=1")


@pytest.fixture
def api_v1(token) -> GgselApiV1:
    return GgselApiMaster(token=token, client=SyncGClient(timeout=TIMEOUT)).api_v1


@pytest.fixture
def api_v2(api_key) -> GgselApiV2:
    return GgselApiMaster(api_key=api_key, client=SyncGClient(timeout=TIMEOUT)).api_v2


def run_async(coro_func, api_key: str = "", token: str = ""):
    """
    Runs `coro_func(api)` with an asynchronous `GgselApiMaster` and closes its connections afterwards.
    Each call gets its own event loop, so the client is created inside it.
    """

    async def main():
        client = AsyncGClient(timeout=TIMEOUT)
        async with client:
            return await coro_func(GgselApiMaster(api_key=api_key, token=token, client=client))

    return asyncio.run(main())


@pytest.fixture
def run_async_v1(token):
    return lambda coro_func: run_async(lambda api: coro_func(api.api_v1), token=token)


@pytest.fixture
def run_async_v2(api_key):
    return lambda coro_func: run_async(lambda api: coro_func(api.api_v2), api_key=api_key)
