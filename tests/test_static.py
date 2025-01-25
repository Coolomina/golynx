from http import HTTPStatus

from starlette.applications import Starlette
from starlette.testclient import TestClient
from starlette.routing import Mount
from golynx.config import DatabaseType
from starlette.staticfiles import StaticFiles

from golynx.infrastructure.database.base import BaseDatabase
from golynx.infrastructure.database.provider import DatabaseProvider
from golynx.infrastructure.storage.storage import Storage
from golynx.services.data_flusher import DataFlusher
from golynx.services.link_manager import LinkManager
from .fixtures.database import FakeStorage

storage: Storage = FakeStorage()
database_provider = DatabaseProvider(DatabaseType.IN_MEMORY).get()
database: BaseDatabase = database_provider()
database.initialize(storage=storage)
link_manager = LinkManager(database=database)
data_flusher = DataFlusher(database=database)


routes = [
    Mount("/", app=StaticFiles(directory="golynx/static", html=True), name="static"),
]
app = Starlette(debug=True, routes=routes)
client = TestClient(app)


def test_default_route_returns_200():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
