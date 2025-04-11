from typing import Literal

from pydantic_settings import BaseSettings
from pydantic import computed_field


class Config(BaseSettings):
    SERVICE_HOST: str
    SERVICE_NAME: str
    SERVICE_PASSWORD: str

    RABBITMQ_PORT: int

    POSTGRES_PORT: int
    POSTGRES_DATABASE: str

    MODE: Literal["Dev", "Prod"]
    VERSION: str

    @computed_field
    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://postgres:{self.SERVICE_PASSWORD}@{self.SERVICE_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"

    @computed_field
    @property
    def RABBITMQ_URL(self):
        return f"aqmp://{self.SERVICE_NAME}:{self.SERVICE_PASSWORD}@{self.SERVICE_HOST}:{self.RABBITMQ_PORT}"

    class Config:
        env_file = ".env"
        extra = "ignore"


config = Config()
