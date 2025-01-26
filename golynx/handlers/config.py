from http import HTTPStatus
from golynx.config import Config
from starlette.requests import Request
from starlette.responses import JSONResponse

class ConfigHandler:
  def __init__(self):
    self.database = Config.DATABASE
    self.by_pass_oauth_proxy = Config.BYPASS_OAUTH_PROXY

  async def get_all(self, request: Request):
    return JSONResponse(
      {
        "database": self.database.value,
        "by_pass_oauth_proxy": self.by_pass_oauth_proxy
      },
      status_code=HTTPStatus.OK
    )
