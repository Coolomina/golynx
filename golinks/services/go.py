import logging
from starlette.responses import JSONResponse
from starlette.requests import Request

logger = logging.getLogger("services/go")

async def hello(request: Request):
    try:
        mail = request.headers['x-forwarded-email']
        logger.info(f"Authenticated user with mail {mail} used the service")
    except KeyError:
        return JSONResponse({"message": "Hello from go service"})
    return JSONResponse({"message": "Hello from go service", "user": mail})
