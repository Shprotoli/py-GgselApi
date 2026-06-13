from dataclasses import dataclass

from schemas.ggsel_object import GgselChatObject


@dataclass
class MessageItem:
    id: int
    message: str
    buyer: int
    seller: int
    deleted: int
    date_written: str
    date_seen: str
    is_file: int
    filename: str
    url: str
    is_img: int
    preview: str


@dataclass
class MessagesObject(GgselChatObject):
    messages: list[MessageItem]