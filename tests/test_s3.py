from unittest import TestCase
from unittest.mock import MagicMock

from golynx.infrastructure.storage.s3 import S3Storage


class TestS3(TestCase):
    def test_s3_storage_initializes_with_default_bucket(self):
        storage = S3Storage(
            s3_client=MagicMock(),
        )
        assert storage.bucket == S3Storage.DEFAULT_BUCKET

    def test_s3_storage_initializes_when_path_does_not_exist(self):
        s3_client = MagicMock()
        s3_client.get_object.side_effect = Exception("Test exception")

        S3Storage(
            s3_client=s3_client,
        )

        s3_client.put_object.assert_called_once_with(
            Bucket="golynx",
            Key="data",
            Body=b"\x80\x04}\x94.",
            ContentType="application/octet-stream",
        )

    def test_s3_storage_initializes_when_path_exists(self):
        s3_client = MagicMock()
        s3_client.get_object.return_value = {"Body": MagicMock(read=lambda: b"{}")}

        storage = S3Storage(
            s3_client=s3_client,
        )

        assert storage.get() == b"{}"

    def test_s3_storage_writes_data(self):
        s3_client = MagicMock()
        storage = S3Storage(
            s3_client=s3_client,
        )

        storage.write(b"{}")
        s3_client.put_object.assert_called_once_with(
            Bucket="golynx",
            Key="data",
            Body=b"{}",
            ContentType="application/octet-stream",
        )
