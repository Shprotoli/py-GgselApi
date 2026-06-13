from dataclasses import dataclass

from schemas.ggsel_object import GgselObject


@dataclass
class ReviewItem:
    id: int
    info: str
    good: int
    type: str
    date: str
    invoice_id: int
    name: str
    comment: str
    owner_id: int


@dataclass
class ReviewsObject(GgselObject):
    retdesc: str
    totalPages: int
    totalItems: int
    totalGood: int
    totalBad: int
    reviews: list[ReviewItem]