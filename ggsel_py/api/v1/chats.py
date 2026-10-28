# Requests of the `Chats` category of the GGSel API
from ggsel_py.api.category import Category, AsyncCategory, RouteApiV1, RequestSpec, build_request, endpoint
from ggsel_py.parameters.api import EnumCrudMethod
from ggsel_py.schemas.v1.chats_object import ChatsObject
from ggsel_py.schemas.v1.messages_object import MessagesObject

MAX_MESSAGES_COUNT = 100


class ChatsEndpointsV1(Category, RouteApiV1):
    @endpoint(None)
    def create_message_without_file(self, id_i: int, message: str) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/create-message-without-file
        This method sends a message to the order chat. Please note that `id_i` is the ID of the ORDER, not `chat_id`!

        :param id_i: Order number
        :param message: The message you want to send to the order chat
        :return: The API returns no JSON on success, so the result describes the response itself:
                    1) 200 - The message has been sent
                    2) 400/422 - Invalid argument (see .text)
        """
        return build_request(
            EnumCrudMethod.POST,
            "debates/v2",
            params={"id_i": id_i},
            payload={"message": message},
        )

    @endpoint(MessagesObject)
    def list_messages(
            self,
            id_i: int,
            id_from: int | str = "",
            id_to: int | str = "",
            newer: int | bool = False,
            count: int = 10
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/list-of-messages
        This method returns a list of messages for the specified order.

        :param id_i: Order number
        :param id_from: Filter messages with an id not less than the specified one
        :param id_to: Filter messages with an id no larger than the specified one
        :param newer: {1 or 0}
                If the value is 1, it returns messages that have not yet been viewed (not read).
                If the value is 0, it returns only read messages
        :param count: {count <= 100} Number of messages, larger values are reduced to 100
        """
        params = {
            "id_i": id_i,
            "id_from": id_from,
            "id_to": id_to,
            "newer": int(newer),
            "count": min(count, MAX_MESSAGES_COUNT),
        }

        return build_request(EnumCrudMethod.GET, "debates/v2", params=params)

    @endpoint(ChatsObject)
    def list_chats(
            self,
            filter_new: int | bool = 0,
            email: str = "",
            id_ds: str = "",
            pagesize: int = 20,
            page: int = 1,
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/list-of-chats

        :param filter_new: {1 or 0}
                If the value is 1, it returns messages that have not yet been viewed (not read).
                If the value is 0, it returns only read messages
        :param email: [NOT WORKING] Buyer's Email address
        :param id_ds: [NOT WORKING] Discussion ID
        :param pagesize: Number of chats returned
        """
        params = {
            "filter_new": int(filter_new),
            "email": email,
            "id_ds": id_ds,
            "pagesize": pagesize,
            "page": page,
        }

        return build_request(EnumCrudMethod.GET, "debates/v2/chats", params=params)


class Chats(ChatsEndpointsV1):
    pass


class AsyncChats(AsyncCategory, ChatsEndpointsV1):
    pass
