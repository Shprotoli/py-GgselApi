from dataclasses import dataclass
from enum import StrEnum


class Type(StrEnum):
    PERCENTPLUS = "percentplus"
    PERCENTMINUS = "percentminus"
    PRICEMINUS = "priceminus"
    PRICEPLUS = "priceplus"


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