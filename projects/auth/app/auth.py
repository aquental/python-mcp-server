from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request

# The expected API key value for authentication
API_KEY = "super_secret_value"

# The HTTP header name where the API key should be supplied
HEADER = "X-API-Key"


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Try to get the API key from the header
        supplied = request.headers.get(HEADER)

        # If the supplied API key does not match, return a 401 Unauthorized response
        if supplied != API_KEY:
            return JSONResponse(content={"detail": "Invalid API key"}, status_code=401)

        # If the API key is valid, continue processing the request
        return await call_next(request)
