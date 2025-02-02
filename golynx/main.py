import asyncio
import contextlib
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware

from golynx.handlers import config as config_handler
from golynx.infrastructure.database.base import BaseDatabase
from golynx.infrastructure.database.provider import DatabaseProvider
from golynx.infrastructure.storage.disk import Disk
from golynx.infrastructure.storage.provider import StorageProvider
from golynx.middlewares.oauth_check import OauthCheckMiddleware
from golynx.services.data_flusher import DataFlusher

from .handlers.go import Go
from .handlers.api import API
from .infrastructure.logger import initialize_logger
from .services.link_manager import LinkManager
from .routes import ApiRoutes, ConfigRoutes, GoRoutes
from .config import Config

logger = initialize_logger()

storage = StorageProvider(Config.STORAGE).get()
database_provider = DatabaseProvider(Config.DATABASE).get()
database: BaseDatabase = database_provider()
database.initialize(storage=storage)

link_manager = LinkManager(database=database)
data_flusher = DataFlusher(database=database)

go = Go(link_manager=link_manager)
api = API(link_manager=link_manager)
config = config_handler.ConfigHandler()
routes = [
    # Order matters
    Route(GoRoutes.link, endpoint=go.redirect),
    Route(ApiRoutes.golinks, endpoint=api.get_all),
    Route(ConfigRoutes.base, endpoint=config.get_all),
    Route(ApiRoutes.golink_update, endpoint=api.update, methods=["PUT"]),
    Route(ApiRoutes.golink_delete, endpoint=api.delete, methods=["DELETE"]),
    Mount("/", app=StaticFiles(directory="golynx/static", html=True), name="static"),
]

middleware = []
if not Config.BYPASS_OAUTH_PROXY:
    middleware.append(Middleware(OauthCheckMiddleware))
    logger.info(f"Registered middlewares: {middleware}")


@contextlib.asynccontextmanager
async def lifespan(app):
    asyncio.create_task(data_flusher.run())
    yield
    data_flusher.stop()


app = Starlette(debug=True, routes=routes, lifespan=lifespan)
