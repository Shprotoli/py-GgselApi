from abc import ABC
from dataclasses import dataclass


class GgselGlobalObject(ABC):
    pass


@dataclass
class GgselObject(GgselGlobalObject):
    retval: int


@dataclass
class GgselChatObject(GgselGlobalObject):
    pass
