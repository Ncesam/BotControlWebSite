import re

from aiohttp._websocket.reader_c import Optional
from pydantic import BaseModel, field_validator

from src.API.Auth.exceptions import PasswordInvalid


class User(BaseModel):
    email: str
    password: str

    @field_validator("password", mode="after")
    @classmethod
    def validate_password(cls, value):
        if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", value):
            return value
        else:
            raise PasswordInvalid()


class UserDB(BaseModel):
    email: str
    nickname: str
    hashed_password: str
    refresh_token: Optional[str] = None
