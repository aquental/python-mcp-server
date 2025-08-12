import uvicorn
from fastapi import FastAPI
from starlette.middleware import Middleware
from auth import ApiKeyMiddleware
from shopping_list import ShoppingListService
from mcp_server import mcp  # Import the MCP server with tools

# Create the FastAPI app and add middleware
app = FastAPI(
    middleware=[Middleware(ApiKeyMiddleware)]
)

# Create a shopping list service instance
shopping_list = ShoppingListService()


@app.get("/items/")
async def get_all_items():
    """Get all shopping list items."""
    return shopping_list.get_items()

# Mount the MCP SSE app at '/mcp'
app.mount('/mcp', mcp.sse_app())

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
        reload=True
    )
