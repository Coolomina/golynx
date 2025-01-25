from golynx.config import DatabaseType
from golynx.infrastructure.database.base import BaseDatabase
from golynx.infrastructure.database.in_memory import InMemoryDatabase
from golynx.infrastructure.database.supabase import SupabaseDatabase


class DatabaseProvider:
    def __init__(self, database: DatabaseType):
        self.database = database

    def get(self) -> type[BaseDatabase]:
        if self.database == DatabaseType.IN_MEMORY:
            return InMemoryDatabase
        elif self.database == DatabaseType.SUPABASE:
            return SupabaseDatabase
        else:
            raise ValueError(f"Invalid database type: {self.database}")
