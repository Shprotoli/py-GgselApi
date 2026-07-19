from abc import ABC
from dataclasses import dataclass


class GgselGlobalObject(ABC):
    def __call__(self, *args, **kwargs):
        pass


@dataclass
class GgselObject(GgselGlobalObject):
    retval: int


@dataclass
class GgselObjectApiV2(GgselGlobalObject):
    VERSION_API: str = "V2"


@dataclass
class GgselChatObject(GgselGlobalObject):
    pass
