from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReplyMessage(BaseModel):
    peerId: int
    messageId: int
    text: str


class Message(BaseModel):
    text: str
    peerId: int
    messageId: int
    reply: Optional[ReplyMessage] = None
    date: datetime
