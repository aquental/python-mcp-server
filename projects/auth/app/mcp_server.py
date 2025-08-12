from mcp.server.fastmcp import FastMCP
from shopping_list import ShoppingListService

# Create the MCP server
mcp = FastMCP(
    name="Shopping List",
    description="Provides tools to manage a shopping list: add items, remove items, mark purchased, and list items",
)

# Create a shopping list service
shopping_list = ShoppingListService()


@mcp.tool()
def add_item(name: str, quantity: int) -> str:
    """
    Add a shopping list item.

    Parameters:
      name (str): The name of the item.
      quantity (int): The quantity to add.

    Returns:
      str: The unique ID of the newly added item.
    """
    return shopping_list.add_item(name, quantity)


@mcp.tool()
def remove_item(item_id: str) -> bool:
    """
    Remove an item from the shopping list.

    Parameters:
      item_id (str): The unique ID of the item.

    Returns:
      bool: True if the item was removed successfully; otherwise False.
    """
    return shopping_list.remove_item(item_id)


@mcp.tool()
def mark_purchased(item_id: str, purchased: bool = True) -> bool:
    """
    Mark an item as purchased or not.

    Parameters:
      item_id (str): The unique ID of the item.
      purchased (bool, optional): True to mark as purchased; False otherwise. Defaults to True.

    Returns:
      bool: True if the update succeeded; otherwise False.
    """
    return shopping_list.set_purchased(item_id, purchased)


@mcp.tool()
def fetch_items(purchased: bool = None) -> list:
    """
    Retrieve all shopping list items, optionally filtered by purchased status.

    Parameters:
        purchased (bool, optional): Filter items by purchased status.
            None returns all items,
            True returns only purchased items,
            False returns only unpurchased items.

    Returns:
        list: A list of shopping items matching the filter criteria.
    """
    return shopping_list.get_items(purchased)
