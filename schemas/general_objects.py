from dataclasses import dataclass
from typing import Any

from schemas.ggsel_object import GgselGlobalObject, GgselObjectApiV2


@dataclass
class UndetectedObject(GgselGlobalObject):
    """
    This object is used when the API result is unexpected
    """
    data: Any | None = None


@dataclass
class PaginationObject:
    total_pages: int
    page: int
    limit: int
    total_count: int


@dataclass
class SuccessObject(GgselObjectApiV2):
    success: bool | None = None
    job_id: str | None = None
