from dataclasses import dataclass

from schemas.ggsel_object import GgselObjectApiV2
from schemas.v2.category_object import CategoryObject


@dataclass
class ListOfPagination:
    total_pages: int
    page: int
    limit: int
    total_count: int


@dataclass
class ListOfCategories(GgselObjectApiV2):
    data: list[CategoryObject] | None = None
    pagination: ListOfPagination | None = None
