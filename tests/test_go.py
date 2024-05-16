from starlette.testclient import TestClient
from golinks.main import app

client = TestClient(app)

def test_default_route_returns_200():
    response = client.get('/')
    assert response.status_code == 200

def test_go_service_returns_200():
    response = client.get('/go')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello from go service'}
    
def test_go_service_parses_user():
    client.headers = {"x-forwarded-email": "pepe@pips.bat"}
    response = client.get('/go')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello from go service', 'user': 'pepe@pips.bat'}

def test_websocket():
    with client.websocket_connect('/cable') as websocket:
        websocket.send_text('test')
        data = websocket.receive_text()
        assert data == 'Received: test'