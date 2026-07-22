from dataclasses import dataclass

from schemas.ggsel_object import GgselObjectApiV2
from schemas.general_objects import PaginationObject
from parameters.options import DiscountType, ImpactType


@dataclass
class VariantEntity:
    id: int
    title_ru: str
    title_en: str
    price: int
    discount_type: str
    impact_type: str
    is_default: bool
    status: str
    position: int
    in_stock_products_count: int
    sold_products_count: int


@dataclass
class OptionEntity:
    id: int
    type: str
    status: str
    title_ru: str
    title_en: str
    comment_ru: str
    comment_en: str
    is_required: bool
    is_price_modifier_hidden: bool
    position: int
    has_splitted_products: bool
    variants: list[VariantEntity] = None


@dataclass
class OptionObject(GgselObjectApiV2):
    data: OptionEntity | None = None
    pagination: PaginationObject | None = None


@dataclass
class OptionValueEntity:
    id: int
    title_ru: str
    title_en: str
    price: float | int
    discount_type: DiscountType | str
    impact_type: ImpactType | str
    is_default: bool | str
    status: str
    position: int


@dataclass
class OptionValueObject(GgselObjectApiV2):
    data: OptionValueEntity | None = None


@dataclass
class SuccessObject(GgselObjectApiV2):
    success: bool | None = None
    job_id: str | None = None
