from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_NAME: str = Field(alias='DATABASE_NAME')
    DB_PASS: str = Field(alias='DATABASE_PASS')
    DB_USER: str = Field(alias='DATABASE_USER')
    DB_HOST: str = Field(alias='DATABASE_HOST')
    DB_PORT: str = Field(alias='DATABASE_PORT')

    @property
    def database_url(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?async_fallback=True' # noqa E501
