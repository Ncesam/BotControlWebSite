from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    text: str
    peerId: int
    messageId: int
    date: datetime
