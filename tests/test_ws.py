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

def test_websocket():
    with client.websocket_connect('/cable') as websocket:
        websocket.send_text('test')
        data = websocket.receive_text()
        assert data == 'Received: test'