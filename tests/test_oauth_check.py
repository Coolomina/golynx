from http import HTTPStatus
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient
from golynx.middlewares.oauth_check import OauthCheckMiddleware

async def stub(request: Request):
    return JSONResponse({})

app = Starlette(routes=[Route('/', endpoint=stub )], middleware=[Middleware(OauthCheckMiddleware)])
client = TestClient(app)

def test_header_check():
    response = client.get('/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED