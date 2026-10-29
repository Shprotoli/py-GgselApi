from dataclasses import dataclass
from enum import StrEnum

from ggsel_py.parameters.common import AsDictMixin


class Type(StrEnum):
    PERCENTPLUS = "percentplus"
    PERCENTMINUS = "percentminus"
    PRICEMINUS = "priceminus"
    PRICEPLUS = "priceplus"


class OrderCol(StrEnum):
    ORDER_COL = "order_col"


class OrderDir(StrEnum):
    ASC = "asc"
    DESC = "desc"


@dataclass
class Variant:
    variant_id: int
    rate: int
    type: str | Type

    def as_dict(self) -> dict:
        return {
            "variant_id": self.variant_id,
            "rate": self.rate,
            "type": self.type,
        }


class StatusProduct(StrEnum):
    IN_STOCK = "in_stock"
    SOLD = "sold"


@dataclass
class ProductParametr:
    value: str


@dataclass
class ProductList(AsDictMixin):
    products: list[ProductParametr | dict]


ProductListType = ProductList | dict[str, list[ProductParametr]]
