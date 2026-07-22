from dataclasses import dataclass

from schemas.ggsel_object import GgselObjectApiV2
from schemas.v2.category_object import CategoryObject
from schemas.general_objects import PaginationObject


@dataclass
class ListOfCategories(GgselObjectApiV2):
    data: list[CategoryObject] | None = None
    pagination: PaginationObject | None = None
