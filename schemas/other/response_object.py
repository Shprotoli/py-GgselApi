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
class ErrorResponseObject(UnknownResponseObject):
    # Status code is 4xx
    text: str
    headers: dict[str, str]


@dataclass
class CompletedResponseObject(UnknownResponseObject):
    # Status code is 2xx
    headers: dict[str, str]


ResponseApiResult = UnknownResponseObject | JSONErrorResponseObject | CompletedResponseObject | ErrorResponseObject
