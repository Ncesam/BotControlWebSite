from typing import Literal

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    POSTGRES_URL: str
    MODE: Literal["Dev", "Prod"]
    VERSION: str

    class Config:
        env_file = ".env"
        extra = "ignore"


config = Config()
