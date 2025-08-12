from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request

# The expected API key value for authentication
API_KEY = "super_secret_value"

# The HTTP header name where the API key should be supplied
HEADER = "X-API-Key"

# The prefix where the MCP server is mounted
MCP_PREFIX = "/mcp"


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if the request path starts with the MCP prefix
        if request.url.path.startswith(MCP_PREFIX):
            # Only check for the API key if accessing MCP routes
            supplied = request.headers.get(HEADER)

            # If the supplied API key does not match, return a 401 Unauthorized response
            if supplied != API_KEY:
                return JSONResponse(content={"detail": "Invalid API key"}, status_code=401)

        # If the API key is valid or the route doesn't require authentication, continue processing
        return await call_next(request)
