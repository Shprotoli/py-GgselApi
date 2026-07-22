from dataclasses import dataclass
from typing import Any

from schemas.ggsel_object import GgselGlobalObject


@dataclass
class UndetectedObject(GgselGlobalObject):
    """
    This object is used when the API result is unexpected
    """
    data: dict[str, Any] | None = None


@dataclass
class PaginationObject:
    total_pages: int
    page: int
    limit: int
    total_count: int
