import pytest

from golynx.infrastructure.database import Database
from golynx.infrastructure.storage.storage import Storage

database = Database()

@pytest.fixture
def setup_database():
    storage = FakeStorage()
    database.initialize(storage)
    yield
    database._data = {}

class FakeStorage(Storage):
    def __init__(self) -> None:
        pass
    def get(self) -> dict:
        return {}
    def write(self, data: dict):
        pass
