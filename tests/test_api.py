from http import HTTPStatus
from unittest import TestCase
from starlette.routing import Route

from starlette.applications import Starlette
from starlette.testclient import TestClient
from golynx.config import DatabaseType
from golynx.handlers.api import API
from golynx.handlers.go import Go
from golynx.infrastructure.database.base import BaseDatabase
from golynx.infrastructure.database.provider import DatabaseProvider
from golynx.infrastructure.storage.storage import Storage
from golynx.services.data_flusher import DataFlusher
from golynx.services.link_manager import LinkManager
from .fixtures.database import FakeStorage
from golynx.routes import ApiRoutes, GoRoutes


class TestApi(TestCase):
    def setUp(self):
        self.storage: Storage = FakeStorage()
        self.database_provider = DatabaseProvider(DatabaseType.IN_MEMORY).get()
        self.database: BaseDatabase = self.database_provider()
        self.database.initialize(storage=self.storage)
        self.link_manager = LinkManager(database=self.database)
        self.data_flusher = DataFlusher(database=self.database)
        self.go = Go(link_manager=self.link_manager)
        self.api = API(link_manager=self.link_manager)
        self.routes = [
            Route(GoRoutes.link, endpoint=self.go.redirect),
            Route(ApiRoutes.golinks, endpoint=self.api.get_all),
            Route(ApiRoutes.golink_update, endpoint=self.api.update, methods=["PUT"]),
            Route(
                ApiRoutes.golink_delete, endpoint=self.api.delete, methods=["DELETE"]
            ),
        ]
        self.app = Starlette(debug=True, routes=self.routes)
        self.client = TestClient(self.app)

    def test_api_update_returns_201(self):
        response = self.client.put(
            url=ApiRoutes.golink_update, json={"link": "lol", "redirection": "lolo"}
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {"message": "ok"}

    def test_api_update_returns_400_when_missing_redir_in_body(self):
        response = self.client.put(url=ApiRoutes.golink_update, json={"link": "lol"})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "message": "missing 'redirection' field in the request body"
        }

    def test_api_update_returns_400_when_missing_link_in_body(self):
        response = self.client.put(
            url=ApiRoutes.golink_update, json={"redirection": "lol"}
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "message": "missing 'link' field in the request body"
        }

    def test_api_delete_returns_200(self):
        self.client.put(
            url=ApiRoutes.golink_update, json={"link": "lol", "redirection": "lolo"}
        )
        response = self.client.delete(url=ApiRoutes.golink_delete.format(link="lol"))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"message": "deleted"}

    def test_api_get_all_golinks_returns_200(self):
        response = self.client.get(ApiRoutes.golinks)
        assert response.status_code == HTTPStatus.OK
