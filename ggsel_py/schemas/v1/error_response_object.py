from dataclasses import dataclass

from ggsel_py.schemas.ggsel_object import GgselObject


@dataclass
class ErrorResponseObject(GgselObject):
    retdesc: str
