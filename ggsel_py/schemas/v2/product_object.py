from dataclasses import dataclass

from ggsel_py.schemas.ggsel_object import GgselObjectApiV2


@dataclass
class ProductObject(GgselObjectApiV2):
    id: int | None = None
    value: str | None = None
    status: str | None = None
    created_at: str | None = None
