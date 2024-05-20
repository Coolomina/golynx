from starlette.routing import WebSocketRoute
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from .handlers.go import Go
from .handlers import cable
from .infrastructure.logger import initialize_logger
from .infrastructure.database import Database
from .services.link_manager import LinkManager

logger = initialize_logger()
database: Database = Database().initialize()
link_manager = LinkManager(database=database)

go = Go(link_manager=link_manager)

routes = [
    # Order matters
    Route('/go/{link}', endpoint=go.redirect),
    Route('/go', endpoint=go.update, methods=["PUT"]),
    Route('/go/{link}', endpoint=go.delete, methods=["DELETE"]),
    WebSocketRoute("/cable", endpoint=cable.websocket_endpoint),
    Mount('/', app=StaticFiles(directory='golinks/static', html=True), name="static"),
]
app = Starlette(debug=True, routes=routes)