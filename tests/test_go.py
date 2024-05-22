from http import HTTPStatus

from starlette.testclient import TestClient
from golynx.main import app
from golynx.infrastructure.database import Database
from .fixtures.database import setup_database

client = TestClient(app)

def test_default_route_returns_200():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK

def test_go_get_returns_307(setup_database):
    response = client.get('/go/test', follow_redirects=False)
    assert response.status_code == HTTPStatus.TEMPORARY_REDIRECT

def test_go_update_returns_201(setup_database):
    response = client.put(url='/go', json={'link':'lol','redirection':'lolo'})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"message":"ok"}

def test_go_update_returns_400_when_missing_body():
    response = client.put(url='/go', json={'link':'lol'})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'message': "missing 'redirection' field in the request body"}

def test_go_delete_returns_200():
    client.put(url='/go', json={'link':'lol','redirection':'lolo'})
    response = client.delete(url='/go/lol')
    assert response.status_code == 200
    assert response.json() == {'message': 'deleted'}

def test_websocket():
    with client.websocket_connect('/cable') as websocket:
        websocket.send_text('test')
        data = websocket.receive_text()
        assert data == 'Received: test'
