# Requests of the `Async jobs` group of the GGSel API V2
from ggsel_py.api.category import Category, AsyncCategory, RouteApiV2, RequestSpec, build_request, endpoint
from ggsel_py.parameters.api import EnumCrudMethod
from ggsel_py.schemas.v2.async_job_result_object import AsyncJobResultObject


class AsyncJobsEndpointsV2(Category, RouteApiV2):
    @endpoint(AsyncJobResultObject)
    def get_async_job_result(self, job_id: str) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/get-async-job-result
        Returns the state of a background task (for example, the `job_id` returned by
        `options.archive_option_variants_asynchronously`). `status` is one of `AsyncJobStatus`.
        """
        return build_request(EnumCrudMethod.GET, f"async_job_results/{job_id}")


class AsyncJobs(AsyncJobsEndpointsV2):
    pass


class AsyncAsyncJobs(AsyncCategory, AsyncJobsEndpointsV2):
    pass
