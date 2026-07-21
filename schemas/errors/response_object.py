from dataclasses import dataclass

from schemas.ggsel_object import GgselGlobalObject


@dataclass
class ResponseErrorObject(GgselGlobalObject):
    status_code: int
    url: str
    method: str


@dataclass
class ResponseJSONErrorObject(ResponseErrorObject):
    text: str
    headers: dict
