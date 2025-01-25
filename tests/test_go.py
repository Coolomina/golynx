from http import HTTPStatus

from starlette.applications import Starlette
from starlette.testclient import TestClient
from starlette.routing import Route
from golynx.config import DatabaseType
from golynx.handlers.go import Go
from golynx.infrastructure.database.base import BaseDatabase
from golynx.infrastructure.database.provider import DatabaseProvider
from golynx.infrastructure.storage.storage import Storage
from golynx.services.link_manager import LinkManager
from golynx.routes import GoRoutes
from .fixtures.database import FakeStorage, setup_database

storage: Storage = FakeStorage()
database_provider = DatabaseProvider(DatabaseType.IN_MEMORY).get()
database: BaseDatabase = database_provider()
database.initialize(storage=storage)
link_manager = LinkManager(database=database)
routes = [
    Route(GoRoutes.link, endpoint=Go(link_manager=link_manager).redirect),
]
app = Starlette(debug=True, routes=routes)
client = TestClient(app)


def test_go_get_returns_307(setup_database):
    response = client.get(GoRoutes.link.format(link="pepito"), follow_redirects=False)
    assert response.status_code == HTTPStatus.TEMPORARY_REDIRECT
