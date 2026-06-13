from dataclasses import dataclass

from schemas.ggsel_object import GgselObject


@dataclass
class OfferSearchPages:
    name: int
    rows: int


@dataclass
class OfferSearchSnippets:
    info: str
    name: str


@dataclass
class OfferSearchSaleInfo:
    common_base_price: int
    common_price_usd: int
    common_price_eur: int
    common_price_uah: int


@dataclass
class OfferSearchProduct:
    id: int
    name: str
    price: int
    snippets: OfferSearchSnippets
    sale_info: OfferSearchSaleInfo
    sale_percent: int


@dataclass
class OfferSearchObject(GgselObject):
    retdesc: str
    pages: OfferSearchPages
    products: list[OfferSearchProduct]