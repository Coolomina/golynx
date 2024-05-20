import asyncio
import contextlib
from starlette.routing import WebSocketRoute
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from golinks.services.data_flusher import DataFlusher

from .handlers.go import Go
from .handlers import cable
from .infrastructure.logger import initialize_logger
from .infrastructure.database import Database
from .services.link_manager import LinkManager

logger = initialize_logger()
database: Database = Database().initialize()
link_manager = LinkManager(database=database)
data_flusher = DataFlusher(database=database)

go = Go(link_manager=link_manager)
routes = [
    # Order matters
    Route('/go/{link}', endpoint=go.redirect),
    Route('/go', endpoint=go.update, methods=["PUT"]),
    Route('/go/{link}', endpoint=go.delete, methods=["DELETE"]),
    WebSocketRoute("/cable", endpoint=cable.websocket_endpoint),
    Mount('/', app=StaticFiles(directory='golinks/static', html=True), name="static"),
]

@contextlib.asynccontextmanager
async def lifespan(app):
    asyncio.create_task(data_flusher.run())
    yield
    data_flusher.stop()

app = Starlette(debug=True, routes=routes, lifespan=lifespan)