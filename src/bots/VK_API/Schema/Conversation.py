from pydantic import BaseModel


class Conversation(BaseModel):
    peerId: int
    conversationType: str
    textLastMessage: str
