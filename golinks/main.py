from starlette.routing import WebSocketRoute
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from .infrastructure.logger import initialize_logger
from .services import go, cable

logger = initialize_logger()

routes = [
    # Order matters
    Route("/go", endpoint=go.hello),
    WebSocketRoute("/cable", endpoint=cable.websocket_endpoint),
    Mount('/', app=StaticFiles(directory='golinks/static', html=True), name="static"),
]
app = Starlette(debug=True, routes=routes)