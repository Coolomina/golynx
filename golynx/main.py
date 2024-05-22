import asyncio
import contextlib
from starlette.routing import WebSocketRoute
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from golynx.infrastructure.storage.disk import Disk
from golynx.services.data_flusher import DataFlusher

from .handlers.go import Go
from .handlers.api import API
from .handlers import cable
from .infrastructure.logger import initialize_logger
from .infrastructure.database import Database
from .services.link_manager import LinkManager

logger = initialize_logger()
storage: Disk = Disk()
database: Database = Database().initialize(storage=storage)
link_manager = LinkManager(database=database)
data_flusher = DataFlusher(database=database)

go = Go(link_manager=link_manager)
api = API(link_manager=link_manager)

routes = [
    # Order matters
    Route('/api', endpoint=api.get_all),
    Route('/go/{link}', endpoint=go.redirect),
    Route('/api/golink', endpoint=api.update, methods=["PUT"]),
    Route('/api/golink/{link}', endpoint=api.delete, methods=["DELETE"]),
    WebSocketRoute("/cable", endpoint=cable.websocket_endpoint),
    Mount('/', app=StaticFiles(directory='golynx/static', html=True), name="static"),
]

@contextlib.asynccontextmanager
async def lifespan(app):
    asyncio.create_task(data_flusher.run())
    yield
    data_flusher.stop()

app = Starlette(debug=True, routes=routes, lifespan=lifespan)