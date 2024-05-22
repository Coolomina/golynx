from http import HTTPStatus

from starlette.applications import Starlette
from starlette.testclient import TestClient
from golynx.infrastructure.database import Database
from golynx.infrastructure.storage.storage import Storage
from golynx.main import routes, lifespan
from golynx.services.data_flusher import DataFlusher
from golynx.services.link_manager import LinkManager
from .fixtures.database import FakeStorage, setup_database

storage: Storage = FakeStorage()
database: Database = Database().initialize(storage=storage)
link_manager = LinkManager(database=database)
data_flusher = DataFlusher(database=database)
app = Starlette(debug=True, routes=routes, lifespan=lifespan)
client = TestClient(app)

def test_api_update_returns_201(setup_database):
    response = client.put(url='/api/golink', json={'link':'lol','redirection':'lolo'})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"message":"ok"}

def test_api_update_returns_400_when_missing_body():
    response = client.put(url='/api/golink', json={'link':'lol'})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'message': "missing 'redirection' field in the request body"}

def test_api_delete_returns_200():
    client.put(url='/api/golink', json={'link':'lol','redirection':'lolo'})
    response = client.delete(url='/api/golink/lol')
    assert response.status_code == 200
    assert response.json() == {'message': 'deleted'}
