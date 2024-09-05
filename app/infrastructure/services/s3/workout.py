from dataclasses import dataclass
from io import BytesIO

from infrastructure.services.s3.base import BaseS3Service


@dataclass
class WorkoutS3Service(BaseS3Service):
    bucket_name: str

    async def upload_file(self, file: BytesIO, file_name: str) -> str:
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=file,
            )

        return self.config.s3_workout_file_path_form.format(file_name=file_name)
