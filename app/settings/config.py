from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    algorithm: str = Field(alias='ALGORITHM')
    secret_key: str = Field(alias='SECRET_KEY')
    token_expire_min: int = Field(alias='TOKEN_EXPIRE_TIME')

    DB_NAME: str = Field(alias='DATABASE_NAME')
    DB_PASS: str = Field(alias='DATABASE_PASS')
    DB_USER: str = Field(alias='DATABASE_USER')
    DB_HOST: str = Field(alias='DATABASE_HOST')
    DB_PORT: str = Field(alias='DATABASE_PORT')

    s3_access_key_id: str = Field(alias='S3_ACCESS_KEY_ID')
    s3_secret_key: str = Field(alias='S3_SECRET_KEY')
    s3_workout_bucket_name: str = Field(alias='WORKOUT_BUCKET_NAME')
    s3_endpoint_url: str = Field(alias='ENDPOINT_URL')

    s3_workout_file_path_form: str = Field(default='https://77169c2e-c2cb-4c89-bae5-9015b205f8c6.selstorage.ru/{file_name}') # noqa E501

    @property
    def database_url(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?async_fallback=True' # noqa E501
