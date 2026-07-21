from json import dumps
from typing import Any

from parameters.api import EnumCrudMethod
from api.category import Category, RouteApiV1


class ChatsBaseV1(Category, RouteApiV1):
    def _create_message_without_file(self, id_i: int, message: str) -> dict[str, Any]:
        params = {
            "id_i": id_i,
        }
        payload = dumps({
            "message": message,
        })

        return {
            "method": EnumCrudMethod.POST,
            "route": "debates/v2",
            "params": params,
            "data": payload,
        }

    def _list_messages(
            self,
            id_i: int,
            id_from: int | str = "",
            id_to: int | str = "",
            newer: int | bool = False,
            count: int = 10
    ) -> dict[str, Any]:
        params = {
            "id_i": id_i,
            "id_from": id_from,
            "id_to": id_to,
            "newer": int(newer),
            "count": min(count, 100),
        }

        return {
            "method": EnumCrudMethod.GET,
            "route": "debates/v2",
            "params": params,
        }

    def _list_chats(
            self,
            filter_new: int | bool = 0,
            email: str = "",
            id_ds: str = "",
            pagesize: int = 20,
            page: int = 1,
    ) -> dict[str, Any]:
        params = {
            "filter_new": filter_new,
            "email": email,
            "id_ds": id_ds,
            "pagesize": pagesize,
            "page": page,
        }

        return {
            "method": EnumCrudMethod.GET,
            "route": "debates/v2/chats",
            "params": params,
        }
