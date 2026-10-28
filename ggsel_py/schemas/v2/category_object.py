from dataclasses import dataclass

from ggsel_py.schemas.ggsel_object import GgselObjectApiV2


@dataclass
class CategoryObject(GgselObjectApiV2):
    id: int | None = None
    title: str | None = None
    content_type: str | None = None
    fee: int | None = None
    tree: str | None = None
    has_children: bytes | None = None
