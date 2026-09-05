from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from ggsel_py.schemas.ggsel_object import GgselGlobalObject


@runtime_checkable
class ResponseLike(Protocol):
    def json(self) -> Any: ...


@dataclass
class UnknownResponseObject(GgselGlobalObject):
    status_code: int
    url: str
    method: str
    headers: dict[str, str]


@dataclass
class CompletedResponseObject(UnknownResponseObject):
    # Status code is 2xx
    pass


@dataclass
class ErrorsResponseObject(UnknownResponseObject):
    # Status code is 4xx
    text: str


@dataclass
class JSONErrorResponseObject(ErrorsResponseObject):
    # Status code is 401
    pass


ResponseApiResult = UnknownResponseObject | JSONErrorResponseObject | CompletedResponseObject | ErrorsResponseObject
