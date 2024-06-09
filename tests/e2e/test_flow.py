import pickle
from starlette.applications import Starlette
from starlette.testclient import TestClient
from starlette.routing import Route

from golynx.handlers.api import API
from golynx.infrastructure.database import Database
from golynx.infrastructure.storage.storage import Storage
from golynx.routes import ApiRoutes
from golynx.services.link_manager import LinkManager
from golynx.main import lifespan
from tests.fixtures.database import FakeStorage, setup_database
from tests.fixtures.golinks import DEFAULT_GOLINK


storage: Storage = FakeStorage()
database: Database = Database().initialize(storage=storage)
link_manager = LinkManager(database=database)
api = API(link_manager=link_manager)
routes = [
    Route(ApiRoutes.golink_update, endpoint=api.update, methods=["PUT"]),
    Route(ApiRoutes.golink_delete, endpoint=api.delete, methods=["DELETE"]),
]
app = Starlette(debug=True, routes=routes, lifespan=lifespan)

client = TestClient(app)

def test_api_create():
    client.put(
        url=ApiRoutes.golink_update,
        json={'link':DEFAULT_GOLINK.link,'redirection':DEFAULT_GOLINK.redirection},
    )
    database.flush()
    golynx_db = pickle.loads(storage.get())
    assert golynx_db == { 'lol': DEFAULT_GOLINK }

def test_api_update():
    client.put(
        url=ApiRoutes.golink_update,
        json={'link':DEFAULT_GOLINK.link,'redirection':'pepinos'},
    )
    client.put(
        url=ApiRoutes.golink_update,
        json={'link':DEFAULT_GOLINK.link,'redirection':DEFAULT_GOLINK.redirection},
    )
    database.flush()
    golynx_db = pickle.loads(storage.get())
    assert golynx_db == { 'lol': DEFAULT_GOLINK }

def test_api_delete():
    client.put(
        url=ApiRoutes.golink_update,
        json={'link':DEFAULT_GOLINK.link,'redirection':DEFAULT_GOLINK.redirection},
    )
    client.delete(url=ApiRoutes.golink_delete.format(link=DEFAULT_GOLINK.link))
    database.flush()
    golynx_db = pickle.loads(storage.get())
    assert golynx_db == {}