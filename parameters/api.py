from enum import StrEnum


class EnumCrudMethod(StrEnum):
    GET = "get"
    POST = "post"
    PATCH = "patch"
    DELETE = "delete"
