from typing import Literal

from pydantic_settings import BaseSettings
from pydantic import computed_field


class Config(BaseSettings):
    SERVICE_NAME: str
    SERVICE_PASSWORD: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str

    MODE: Literal["Dev", "Prod"]
    VERSION: str

    @computed_field(return_type=str)
    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.SERVICE_NAME}:{self.SERVICE_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"

    class Config:
        env_file = ".env"
        extra = "ignore"


config = Config()
