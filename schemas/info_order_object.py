from dataclasses import dataclass
from datetime import datetime

from schemas.ggsel_object import GgselObject


@dataclass
class InfoOrderFeedback:
    deleted: bool
    feedback: str
    feedback_type: str
    comment: str


@dataclass
class InfoOrderUniqueCodeState:
    state: int
    date_check: datetime
    date_delivery: datetime
    date_confirmed: datetime
    date_refuted: datetime


@dataclass
class InfoOrderOption:
    id: int
    name: str
    user_data: str
    user_data_id: int


@dataclass
class InfoOrderBuyerInfo:
    payment_method: str
    account: str
    email: str
    phone: str
    skype: str
    whatsapp: str
    ip_address: str
    payment_aggregator: str


@dataclass
class InfoOrderContent:
    item_id: int
    content_id: int
    cart_uid: str
    name: str
    amount: int
    currency_type: str
    invoice_state: int
    purchase_date: datetime
    date_pay: datetime
    agent_id: int
    agent_percent: int
    agent_fee: int
    query_string: str
    unit_goods: str
    cnt_goods: str
    promo_code: str
    bonus_code: str
    feedback: InfoOrderFeedback
    unique_code_state: InfoOrderUniqueCodeState
    options: list[InfoOrderOption]
    buyer_info: InfoOrderBuyerInfo
    owner: int
    day_lock: int
    lock_state: str
    profit: int
    external_order_id: str


@dataclass
class InfoOrderObject(GgselObject):
    retdesc: str
    content: InfoOrderContent