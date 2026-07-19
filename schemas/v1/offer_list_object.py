from dataclasses import dataclass

from schemas.ggsel_object import GgselObject


@dataclass
class OfferSaleInfo:
    common_base_price: int
    common_price_usd: int
    common_price_eur: int
    common_price_rur: int
    sale_end: str
    sale_percent: str


@dataclass
class OfferRow:
    id_goods: int
    name_goods: str
    info_goods: str
    price: str
    currency: str
    add_info: str
    cnt_sell: int
    cnt_return: int
    cnt_goodresponses: int
    cnt_badresponses: int
    price_usd: int
    price_eur: int
    price_uah: int
    price_rur: int
    in_stock: int
    num_in_stock: int
    visible: int
    commiss_agent: str
    has_discount: bool
    num_options: int
    sale_info: OfferSaleInfo


@dataclass
class OfferListObject(GgselObject):
    retdesc: str
    page: int
    count: int
    has_next_page: bool
    has_previous_page: bool
    total_count: int
    total_pages: int
    rows: list[OfferRow]