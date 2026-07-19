from dataclasses import dataclass

from schemas.ggsel_object import GgselObject


@dataclass
class ReceiptsOperation:
    id: int
    type: str
    datetime: str
    percent: int
    price: int
    currency: str
    on_account: int


@dataclass
class ReceiptsProductName:
    locale: str
    value: str


@dataclass
class ReceiptsProduct:
    id: int
    name: list[ReceiptsProductName]
    deleted: bool


@dataclass
class ReceiptsItem:
    account_operation_id: int
    operation: ReceiptsOperation
    owner_id: int
    product: ReceiptsProduct
    code_check_datetime: str
    date_free: str
    free_description: str
    response: str


@dataclass
class ReceiptsContent:
    page: int
    count: int
    has_next_page: bool
    has_previous_page: bool
    total_count: int
    total_pages: int
    items: list[ReceiptsItem]


@dataclass
class ReceiptsObject(GgselObject):
    retdesc: str
    errors: list[str]
    content: ReceiptsContent