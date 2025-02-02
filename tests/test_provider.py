from unittest import TestCase
from unittest.mock import patch
from golynx.config import DatabaseType, StorageType
from golynx.infrastructure.database.in_memory import InMemoryDatabase
from golynx.infrastructure.database.provider import DatabaseProvider
from golynx.infrastructure.database.supabase import SupabaseDatabase
from golynx.infrastructure.storage.disk import Disk
from golynx.infrastructure.storage.provider import StorageProvider
from golynx.infrastructure.storage.s3 import S3Storage


class TestProviders(TestCase):
    def test_database_provider_returns_in_memory_database(self):
        provider = DatabaseProvider(DatabaseType.IN_MEMORY)
        assert provider.get() == InMemoryDatabase

    def test_database_provider_returns_supabase_database(self):
        provider = DatabaseProvider(DatabaseType.SUPABASE)
        assert provider.get() == SupabaseDatabase

    def test_storage_provider_returns_disk_storage(self):
        provider = StorageProvider(StorageType.DISK)
        assert isinstance(provider.get(), Disk)

    @patch("golynx.infrastructure.storage.provider.boto3")
    def test_storage_provider_returns_s3_storage(self, boto3):
        provider = StorageProvider(StorageType.S3)
        assert isinstance(provider.get(), S3Storage)

    @patch("golynx.infrastructure.storage.provider.boto3")
    def test_storage_provider_returns_supabase_storage(self, boto3):
        provider = StorageProvider(StorageType.SUPABASE)
        assert isinstance(provider.get(), S3Storage)
