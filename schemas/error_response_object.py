from dataclasses import dataclass

from schemas.ggsel_object import GgselObject


@dataclass
class ErrorResponseObject(GgselObject):
    retdesc: str


print(ErrorResponseObject(**{
  "retval": 0,
  "retdesc": "string"
}))