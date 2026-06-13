from dataclasses import dataclass

from schemas.ggsel_object import GgselObject


@dataclass
class BalanceContent:
    amount_t_lock: int
    amount_t_free: int
    amount_t_plus: int


@dataclass
class BalanceObject(GgselObject):
    retdesc: str
    errors: list
    content: BalanceContent