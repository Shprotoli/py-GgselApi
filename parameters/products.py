from dataclasses import dataclass
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