from pydantic import BaseModel


class Group(BaseModel):
    peerId: int
    name: str


class Chat(BaseModel):
    peerId: int
    name: str
