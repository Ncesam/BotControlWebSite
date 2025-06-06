from typing import List, Optional

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
    text: Optional[str]


class BaseBotForm(BaseModel):
    title: str
    description: str
    token: str
    group_name: str

class Command(BaseModel):
    id: int
    regex: str
    answer: str
    name: str
    enabled: bool

class BotForm(BaseBotForm):
    answers_type: Optional[str] = None
    nicknames: Optional[str] = None
    text: Optional[str] = None
    ads_delay: Optional[int] = None

class BotUpdateForm(BotForm):
    id: int


class BotParams(BaseModel):
    bot_ids: List[int]
