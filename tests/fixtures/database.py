import pytest

from golinks.infrastructure.database import Database

database = Database()

@pytest.fixture
def setup_database():
    database.initialize()
    yield
    database._data = {}
