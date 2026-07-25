from dataclasses import dataclass

from ggsel_py.schemas.ggsel_object import GgselObject


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
