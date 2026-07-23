from dataclasses import dataclass, asdict
from enum import StrEnum


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

    def as_dict(self):
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
class ProductList:
    products: list[ProductParametr | dict]

    def asdict(self):
        return asdict(self)


ProductListType = ProductList | dict[str, list[ProductParametr, ...]]
