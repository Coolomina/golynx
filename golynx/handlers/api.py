import logging
from http import HTTPStatus
from starlette.responses import JSONResponse
from starlette.requests import Request
from ..models.dto.golink_dto import GolinkDTO

from ..services.link_manager import LinkManager

logger = logging.getLogger("services/api")

class API:
    def __init__(self, link_manager: LinkManager) -> None:
        self.link_manager = link_manager
    
    async def update(self, request: Request):
        body = await request.json()
        link = body.get('link', None)
        if link is None:
            return JSONResponse({'message': 'missing \'link\' field in the request body'}, status_code=HTTPStatus.BAD_REQUEST)
        
        redirection = body.get('redirection', None)
        if redirection is None:
            return JSONResponse({'message': 'missing \'redirection\' field in the request body'}, status_code=HTTPStatus.BAD_REQUEST)
        
        golink_dto = GolinkDTO(**body)
        
        self.link_manager.handle_update(golink_dto.toGolink())
        
        return JSONResponse({'message': 'ok'}, status_code=HTTPStatus.CREATED)
    
    async def get_all(self, request: Request):
        return JSONResponse(self.link_manager.handle_get_all(), status_code=HTTPStatus.OK)
    
    async def delete(self, request: Request):
        link = request.path_params['link']
        self.link_manager.handle_delete(link)
        
        return JSONResponse({'message': 'deleted'}, status_code=HTTPStatus.OK)