from typing import List

from pydantic import BaseModel


class BotDB(BaseModel):
    id: int
    title: str
    description: str
    status: bool
    user_id: int
    token: str
    group_name: str
    nicknames: List[str]
    answers_type: str


class BotForm(BaseModel):
    title: str
    description: str
    token: str
    group_name: str
    answers_type: str
    nicknames: str


class BotUpdateForm(BotForm):
    id: int


class BotParams(BaseModel):
    bot_ids: List[int]
