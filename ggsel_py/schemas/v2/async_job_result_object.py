from dataclasses import dataclass
from typing import Any

from ggsel_py.schemas.ggsel_object import GgselObjectApiV2


@dataclass
class AsyncJobResultObject(GgselObjectApiV2):
    job_id: str | None = None
    status: str | None = None
    results: dict[str, Any] | None = None
