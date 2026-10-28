import asyncio
import json
from unittest.mock import Mock

from ggsel_py import GgselApiMaster, GgselApiV2
from ggsel_py.api.v2.async_jobs import AsyncJobs, AsyncAsyncJobs
from ggsel_py.api.v2.options import Option
from ggsel_py.parameters.api import EnumCrudMethod
from ggsel_py.parameters.options import VisibilityItem, VisibilityStatus
from ggsel_py.schemas.v2.async_job_result_object import AsyncJobResultObject


def test_get_async_job_result(sync_client, response_factory):
    sync_client.request.return_value = response_factory({"job_id": "42", "status": "completed", "results": {}})

    result = AsyncJobs(sync_client).get_async_job_result("42")

    sync_client.request.assert_called_once_with(method=EnumCrudMethod.GET, route="async_job_results/42")
    assert result == AsyncJobResultObject(job_id="42", status="completed", results={})


def test_get_async_job_result_async(async_client, response_factory):
    from unittest.mock import AsyncMock

    async_client.request = AsyncMock(return_value=response_factory({"job_id": "1", "status": "pending", "results": {}}))

    result = asyncio.run(AsyncAsyncJobs(async_client).get_async_job_result("1"))

    assert result.status == "pending"


def test_async_jobs_is_available_from_facades():
    assert isinstance(GgselApiV2().async_jobs, AsyncJobs)
    assert isinstance(GgselApiMaster().async_jobs, AsyncJobs)


def test_batch_update_options_visibility(sync_client):
    api = Option(sync_client)

    request = type(api).batch_update_options_visibility.build(
        api, 7, [VisibilityItem(1, VisibilityStatus.HIDDEN), {"id": 2, "status": "active"}],
    )

    assert request["method"] == EnumCrudMethod.PATCH
    assert request["route"] == "offers/7/options/batch_visibility"
    assert json.loads(request["data"]) == {"options": [{"id": 1, "status": "hidden"}, {"id": 2, "status": "active"}]}


def test_batch_update_variants_visibility(sync_client):
    api = Option(sync_client)

    request = type(api).batch_update_variants_visibility.build(api, 7, 8, [VisibilityItem(3, "active")])

    assert request["route"] == "offers/7/options/8/variants/batch_visibility"
    assert json.loads(request["data"]) == {"variants": [{"id": 3, "status": "active"}]}
