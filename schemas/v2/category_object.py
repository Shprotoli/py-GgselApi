from dataclasses import dataclass

from schemas.ggsel_object import GgselObjectApiV2


@dataclass
class CategoryObject(GgselObjectApiV2):
    id: int = None
    title: str = None
    content_type: str = None
    fee: int = None
    tree: str = None
    has_children: bytes = None
