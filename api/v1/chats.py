# A class file that handles requests from the `Chats` category of the GGSell API
from json import dumps
from typing import Any

from tools.handlers import handler_api, async_handler_api, EnumMethodHandle, ApiResult
from schemas.v1.messages_object import MessagesObject
from schemas.v1.chats_object import ChatsObject
from api.category import Category


class ChatsBase(Category):
    def _create_message_without_file(self, id_i: int, message: str) -> dict[str, Any]:
        params = {
            "id_i": id_i,
        }
        payload = dumps({
            "message": message,
        })

        return {
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
            "route": "debates/v2/chats",
            "params": params,
        }


class Chats(ChatsBase):
    def create_message_without_file(self, id_i: int, message: str) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/create-message-without-file
        This method sends a message to the order chat. Please note that `id_i` is the ID of the ORDER, not `chat_id`!

        :param id_i: Order number
        :param message: The message you want to send to the order chat
        :return: Returns a Response object whose main part is the status_code, which depends on the result of the request:
                    1) 200 - The message has been sent
                    2) 400/422 - Invalid argument (see .text or .json)
        """
        return handler_api(
            EnumMethodHandle.POST,
            self.client,
            self._create_message_without_file,
            None,
            id_i=id_i,
            message=message
        )

    def list_messages(
            self,
            id_i: int,
            id_from: int | str = "",
            id_to: int | str = "",
            newer: int | bool = False,
            count: int = 10
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/list-of-messages
        This method returns a list of messages for the specified order.

        :param id_i: Order number
        :param id_from: Filter messages with an id not less than the specified one
        :param id_to: Filter messages with an id no larger than the specified one
        :param newer: {1 or 0}
                If the value is 1, it returns messages that have not yet been viewed (not read).
                If the value is 0, it returns only read messages
        :param count: {count <= 100} Number of messages
        :return: dataclass MessagesObject containing a json response from the API
        """
        return handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._list_messages,
            MessagesObject,
            id_i=id_i,
            id_from=id_from,
            id_to=id_to,
            newer=newer,
            count=count
        )

    def list_chats(
            self,
            filter_new: int | bool = 0,
            email: str = "",
            id_ds: str = "",
            pagesize: int = 20,
            page: int = 1,
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/list-of-chats
        This method provides information about chats based on specified parameters

        :param filter_new: {1 or 0}
                If the value is 1, it returns messages that have not yet been viewed (not read).
                If the value is 0, it returns only read messages
        :param email: [NOT WORKING] Buyer's Email address
        :param id_ds: [NOT WORKING] Discussion ID
        :param pagesize: Number of chats returned
        :param page: Chats page
        :return:
        """
        return handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._list_chats,
            ChatsObject,
            filter_new=filter_new,
            email=email,
            id_ds=id_ds,
            pagesize=pagesize,
            page=page
        )


class AsyncChats(ChatsBase):
    async def create_message_without_file(self, id_i: int, message: str) -> ApiResult:
        """
        See Chats.create_message_without_file
        """
        return await async_handler_api(
            EnumMethodHandle.POST,
            self.client,
            self._create_message_without_file,
            None,
            id_i=id_i,
            message=message
        )

    async def list_messages(
            self,
            id_i: int,
            id_from: int | str = "",
            id_to: int | str = "",
            newer: int | bool = False,
            count: int = 10
    ) -> ApiResult:
        """
        See Chats.list_messages
        """
        return await async_handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._list_messages,
            MessagesObject,
            id_i=id_i,
            id_from=id_from,
            id_to=id_to,
            newer=newer,
            count=count
        )

    async def list_chats(
            self,
            filter_new: int | bool = 0,
            email: str = "",
            id_ds: str = "",
            pagesize: int = 20,
            page: int = 1,
    ) -> ApiResult:
        """
        See Chats.list_chats
        """
        return await async_handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._list_chats,
            ChatsObject,
            filter_new=filter_new,
            email=email,
            id_ds=id_ds,
            pagesize=pagesize,
            page=page
        )
