from dataclasses import asdict
from typing import Any


class AsDictMixin:
    """Adds `asdict` to a dataclass that is sent as a request body"""

    def asdict(self) -> dict[str, Any]:
        return asdict(self)


def as_request_body(body: Any, list_type: type[AsDictMixin], item_type: type) -> Any:
    """
    Converts a request body given as a list dataclass (`list_type`) or as a single item (`item_type`)
    into a dictionary. Anything else (for example, an already prepared `dict`) is returned unchanged.
    """
    if isinstance(body, list_type):
        return body.asdict()
    if isinstance(body, item_type):
        return list_type([body]).asdict()
    return body


def drop_none(values: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


def archive_payload(ids_field: str, ids: list[int] | int | None, delete_all: bool) -> dict[str, Any]:
    """The body of the `archive_*` methods: GGSel expects `delete_all` as the string "true"/"false" """
    return {
        ids_field: ids,
        "delete_all": str(delete_all).lower(),
    }
