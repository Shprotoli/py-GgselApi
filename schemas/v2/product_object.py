from dataclasses import dataclass

from schemas.ggsel_object import GgselObjectApiV2


@dataclass
class ProductObject(GgselObjectApiV2):
    id: int = None
    value: str = None
    status: str = None
    created_at: str = None
