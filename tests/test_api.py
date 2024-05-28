from http import HTTPStatus
from urllib import response

from starlette.applications import Starlette
from starlette.testclient import TestClient
from golynx.infrastructure.database import Database
from golynx.infrastructure.storage.storage import Storage
from golynx.main import routes, lifespan
from golynx.services.data_flusher import DataFlusher
from golynx.services.link_manager import LinkManager
from .fixtures.database import FakeStorage, setup_database
from golynx.routes import ApiRoutes

storage: Storage = FakeStorage()
database: Database = Database().initialize(storage=storage)
link_manager = LinkManager(database=database)
data_flusher = DataFlusher(database=database)
app = Starlette(debug=True, routes=routes, lifespan=lifespan)
client = TestClient(app)

def test_api_update_returns_201(setup_database):
    response = client.put(url=ApiRoutes.golink_update, json={'link':'lol','redirection':'lolo'})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"message":"ok"}

def test_api_update_returns_400_when_missing_redir_in_body():
    response = client.put(url=ApiRoutes.golink_update, json={'link':'lol'})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'message': "missing 'redirection' field in the request body"}

def test_api_update_returns_400_when_missing_link_in_body():
    response = client.put(url=ApiRoutes.golink_update, json={'redirection':'lol'})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'message': "missing 'link' field in the request body"}

def test_api_delete_returns_200():
    client.put(url=ApiRoutes.golink_update, json={'link':'lol','redirection':'lolo'})
    response = client.delete(url=ApiRoutes.golink_delete.format(link='lol'))
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'deleted'}

def test_api_get_all_golinks_returns_200():
    response = client.get(ApiRoutes.golinks)
    assert response.status_code == HTTPStatus.OK