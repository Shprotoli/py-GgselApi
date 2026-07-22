from dataclasses import dataclass

from schemas.ggsel_object import GgselObjectApiV2
from schemas.v2.category_object import CategoryObject
from schemas.v2.product_object import ProductObject
from schemas.v2.option_object import OptionEntity
from schemas.general_objects import PaginationObject


@dataclass
class ListOfCategories(GgselObjectApiV2):
    data: list[CategoryObject] | None = None
    pagination: PaginationObject | None = None


@dataclass
class ListOfProducts(GgselObjectApiV2):
    data: list[ProductObject] | None = None
    pagination: PaginationObject | None = None


@dataclass
class ListOfOption(GgselObjectApiV2):
    data: list[OptionEntity] | None = None
    pagination: PaginationObject | None = None
