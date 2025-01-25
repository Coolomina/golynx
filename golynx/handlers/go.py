import logging
from http import HTTPStatus
from starlette.requests import Request
from starlette.responses import RedirectResponse

from ..services.link_manager import LinkManager

logger = logging.getLogger("services/go")


class Go:
    def __init__(self, link_manager: LinkManager) -> None:
        self.link_manager = link_manager

    async def redirect(self, request: Request) -> RedirectResponse:
        link = request.path_params["link"]
        redirect = self.link_manager.handle_redirection(link)

        return RedirectResponse(redirect, HTTPStatus.TEMPORARY_REDIRECT)
