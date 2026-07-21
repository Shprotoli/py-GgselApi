from dataclasses import dataclass

from schemas.ggsel_object import GgselObjectApiV2


@dataclass
class ErrorEntity:
    id: int
    resource: str
    description: str


@dataclass
class ErrorsInformation(ErrorEntity):
    code: str
    entity: ErrorEntity | None = None


@dataclass
class ErrorWithEntityObject(GgselObjectApiV2):
    errors: list[ErrorsInformation] | None = None
