from dataclasses import dataclass

from schemas.ggsel_object import GgselObject


@dataclass
class LastSalesProduct:
    id: int
    name: str
    price_rub: int
    price_usd: int
    price_eur: int
    price_uah: int


@dataclass
class LastSaleItem:
    invoice_id: int
    date: str
    product: LastSalesProduct


@dataclass
class LastSalesObject(GgselObject):
    retdesc: str
    sales: list[LastSaleItem]