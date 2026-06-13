from dataclasses import dataclass

from schemas.ggsel_object import GgselObject


@dataclass
class SellerGoodsSaleInfo:
    common_base_price: int
    common_price_usd: int
    common_price_eur: int
    common_price_rur: int
    sale_end: str
    sale_percent: str


@dataclass
class SellerGoodsRow:
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
    sale_info: SellerGoodsSaleInfo


@dataclass
class SellerGoodsListObject(GgselObject):
    retdesc: str
    id_seller: int
    name_seller: str
    cnt_goods: int
    pages: int
    page: int
    order_col: str
    order_dir: str
    rows: list[SellerGoodsRow]