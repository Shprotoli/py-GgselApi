# A class file that handles requests from the `Chats` category of the GGSell API
from json import dumps
from typing import Union

from tools.handlers import handler_response_api, ApiResult
from schemas.messages_object import MessagesObject
from schemas.chats_object import ChatsObject
from api.v1.category import Category


class Chats(Category):
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
        params = {
            "id_i": id_i,
        }
        payload = dumps({
            "message": message,
        })
        response = self.client.post("debates/v2", params=params, data=payload)

        return handler_response_api(None, data=response)

    def list_messages(
            self,
            id_i: int,
            id_from: Union[int | str] = "",
            id_to: Union[int | str] = "",
            newer: Union[int | bool] = False,
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
        params = {
            "id_i": id_i,
            "id_from": id_from,
            "id_to": id_to,
            "newer": int(newer),
            "count": max(count, 100),
        }
        response = self.client.get("debates/v2", params=params)
        data = response.json()

        return handler_response_api(MessagesObject, data=data)

    def list_chats(
            self,
            filter_new: Union[int | bool] = 0,
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
        params = {
            "filter_new": filter_new,
            "email": email,
            "id_ds": id_ds,
            "pagesize": pagesize,
            "page": page,
        }
        response = self.client.get("debates/v2/chats", params=params)
        data = response.json()

        return handler_response_api(ChatsObject, data=data)