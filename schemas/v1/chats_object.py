from dataclasses import dataclass

from schemas.ggsel_object import GgselChatObject


@dataclass
class ChatItem:
    id_i: int
    email: str
    product: int
    last_message: str
    cnt_msg: int
    cnt_new: int


@dataclass
class ChatsObject(GgselChatObject):
    cnt_pages: int
    items: list[ChatItem]