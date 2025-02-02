import logging
from typing import Any
import boto3

from golynx.infrastructure.storage.storage import Storage

logger = logging.getLogger("infrastructure/storage")


class S3Storage(Storage):
    DEFAULT_BUCKET = "golynx"
    DEFAULT_BUCKET_PATH = "data"

    def __init__(
        self,
        bucket: str | None = None,
        s3_client: Any | None = None,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
    ):
        logger.info("Initializing S3 storage")
        self.s3_client = s3_client or boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.bucket = bucket or self.DEFAULT_BUCKET

        try:
            self.get()
        except Exception as e:
            logger.warning(
                f"Path s3://{self.bucket}/{self.DEFAULT_BUCKET_PATH} does not exist"
            )
            self.write(b"\x80\x04}\x94.")

    def get(self) -> bytes:
        response = self.s3_client.get_object(
            Bucket=self.bucket,
            Key=self.DEFAULT_BUCKET_PATH,
        )
        body = response["Body"].read()
        body = body.split(b"\r\n", 1)[-1]  # Remove chunked encoding size prefix
        body = body.rsplit(b"\r\n", 2)[0]  # Remove chunked encoding suffix

        return body

    def write(self, data: bytes) -> None:
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=self.DEFAULT_BUCKET_PATH,
            Body=data,
            ContentType="application/octet-stream",
        )
