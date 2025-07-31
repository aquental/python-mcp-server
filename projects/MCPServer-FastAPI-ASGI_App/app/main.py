import uvicorn
from fastapi import FastAPI
from shopping_list import ShoppingListService

# Create the FastAPI app
app = FastAPI()

# Create a shopping list service instance
shopping_list = ShoppingListService()

# Regular FastAPI route for getting all shopping list items
@app.get("/items/")
async def get_all_items():
    """Get all shopping list items."""
    return shopping_list.get_items()

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
        reload=True
    )
