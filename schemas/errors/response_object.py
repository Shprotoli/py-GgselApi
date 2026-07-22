from dataclasses import dataclass

from schemas.ggsel_object import GgselGlobalObject


@dataclass
class UnknownResponseObject(GgselGlobalObject):
    status_code: int
    url: str
    method: str


@dataclass
class JSONErrorResponseObject(UnknownResponseObject):
    text: str
    headers: dict


@dataclass
class CompletedResponseObject(UnknownResponseObject):
    headers: dict[str, str]


ResponseApiResult = UnknownResponseObject | JSONErrorResponseObject | CompletedResponseObject
