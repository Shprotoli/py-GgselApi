from dataclasses import dataclass

from schemas.ggsel_object import GgselObject


@dataclass
class CategoryItem:
    id: int
    name: str
    sub: list
    cnt: int


@dataclass
class CategoriesObject(GgselObject):
    retdesc: str
    category: list[CategoryItem]