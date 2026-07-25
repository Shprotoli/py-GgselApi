from dataclasses import dataclass
from datetime import datetime

from ggsel_py.schemas.ggsel_object import GgselObject


@dataclass
class TokenObject(GgselObject):
    desc: str
    token: str
    seller_id: int
    valid_thru: datetime