from http import HTTPStatus
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class OauthCheckMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if 'X-Forwarded-Email' not in request.headers:
            return JSONResponse({'message':'unauthorised'}, HTTPStatus.UNAUTHORIZED)
        
        return response