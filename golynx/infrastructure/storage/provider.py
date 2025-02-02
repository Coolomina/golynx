from golynx.config import Config, StorageType
from golynx.infrastructure.storage.disk import Disk
from golynx.infrastructure.storage.s3 import S3Storage
from golynx.infrastructure.storage.storage import Storage
import boto3


class StorageProvider:
    def __init__(self, storage_type: StorageType):
        self.storage_type = storage_type

    def get(self) -> Storage:
        if self.storage_type == StorageType.DISK:
            return Disk(
                flush_dir=Config.STORAGE_FLUSH_DIR,
                flush_file=Config.STORAGE_FLUSH_FILE,
            )
        elif self.storage_type == StorageType.S3:
            return S3Storage(
                bucket=Config.STORAGE_S3_BUCKET,
                s3_client=boto3.client(
                    "s3",
                    aws_access_key_id=Config.STORAGE_S3_AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=Config.STORAGE_S3_AWS_SECRET_ACCESS_KEY,
                ),
            )
        elif self.storage_type == StorageType.SUPABASE:
            return S3Storage(
                bucket=Config.STORAGE_S3_BUCKET,
                s3_client=boto3.client(
                    "s3",
                    endpoint_url=Config.SUPABASE_URL + "/storage/v1/s3",
                    aws_access_key_id=Config.STORAGE_S3_AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=Config.STORAGE_S3_AWS_SECRET_ACCESS_KEY,
                ),
            )
        else:
            raise ValueError(f"Invalid storage type: {self.storage_type}")
