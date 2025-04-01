from typing import List, Optional

from pydantic import BaseModel

from src.API.Bots.schemas import BotDB


class UserParameters(BaseModel):
    user_ids: List[int]
    fields: Optional[List[str]] = ["All"]


class UserInfo(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    nickname: Optional[str] = None
    bots: Optional[List[BotDB]] = None
