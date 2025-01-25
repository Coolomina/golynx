from unittest import TestCase
from golynx.config import DatabaseType
from golynx.infrastructure.database.in_memory import InMemoryDatabase
from golynx.infrastructure.database.provider import DatabaseProvider
from golynx.infrastructure.database.supabase import SupabaseDatabase


class TestProvider(TestCase):
    def test_provider_returns_in_memory_database(self):
        provider = DatabaseProvider(DatabaseType.IN_MEMORY)
        assert provider.get() == InMemoryDatabase

    def test_provider_returns_supabase_database(self):
        provider = DatabaseProvider(DatabaseType.SUPABASE)
        assert provider.get() == SupabaseDatabase
