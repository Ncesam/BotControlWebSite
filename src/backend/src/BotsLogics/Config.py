from pydantic import computed_field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ADS_DELAY: int
    DELAY: int

    SERVICE_PASSWORD: str
    SERVICE_NAME: str

    MONGODB_HOST: str
    MONGODB_PORT: int

    @computed_field(return_type=str)
    @property
    def MONGODB_URL(self):
        return f"mongodb://{self.SERVICE_NAME}:{self.SERVICE_PASSWORD}@{self.MONGODB_HOST}:{self.MONGODB_PORT}/"

    class Config:
        env_file = ".env"
        extra = "ignore"


config = Config()
