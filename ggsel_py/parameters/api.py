from enum import StrEnum


class EnumCrudMethod(StrEnum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"


class ApiVersion(StrEnum):
    V1 = "V1"
    V2 = "V2"


class Header(StrEnum):
    AUTHORIZATION = "Authorization"
    LOCALE = "locale"
    LANG = "lang"


TOKEN_PARAM = "token"


class AsyncJobStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
