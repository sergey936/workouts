from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass
from io import BytesIO

from aiobotocore.session import AioSession
from settings.config import Config


@dataclass
class BaseS3Service(ABC):
    session: AioSession
    config: Config

    access_key: str
    secret_key: str
    endpoint_url: str

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client(
            "s3",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.endpoint_url
        ) as client:
            yield client

    @abstractmethod
    async def upload_file(self, file: BytesIO, file_name: str):
        ...
