from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from core.config import settings
import logging
from starlette.responses import JSONResponse
# from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

class AllowedIPsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request,call_next):
        local_host = "0.0.0.0"
        client_ip = request.client.host if request.client else local_host 
        print(type(client_ip), settings.ALLOWED_IPS, type(settings.ALLOWED_IPS))
        # import ipdb;ipdb.set_trace()
        if client_ip not in settings.ALLOWED_IPS:

            return JSONResponse(
                status_code=403,
                content = {
                    "status": False,
                    "status_code": 403,
                    "error": "Access denied: IP not authorized"
                }
            )
        
        response = await call_next(request)
        return response

