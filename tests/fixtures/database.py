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
        self._fake_disk_info = bytearray()
    def get(self) -> bytes:
        return self._fake_disk_info
    def write(self, data: bytes):
        self._fake_disk_info = data

