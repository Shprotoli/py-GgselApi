from dataclasses import dataclass

from schemas.ggsel_object import GgselObject


@dataclass
class UniqueCodeState:
    state: int
    date_check: str
    date_delivery: str
    date_confirmed: str
    date_refuted: str


@dataclass
class UniqueCodeOption:
    id: int
    name: str
    value: str
    variant_id: int


@dataclass
class UniqueCodeObject(GgselObject):
    retdesc: str
    inv: int
    id_goods: int
    amount: int
    type_curr: str
    amount_usd: int
    profit: int
    date_pay: str
    email: str
    name_invoice: str
    lang: str
    agent_id: int
    agent_percent: str
    query_string: str
    unit_goods: str
    cnt_goods: str
    promo_code: str
    bonus_code: str
    cart_uid: str
    unique_code_state: UniqueCodeState
    options: list[UniqueCodeOption]