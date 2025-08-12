import uuid


class ShoppingListService:
    """Manages a collection of shopping items with basic operations."""

    def __init__(self):
        self.items = [
            {"id": str(uuid.uuid4()), "name": "Milk",
             "quantity": 2, "purchased": True},
            {"id": str(uuid.uuid4()), "name": "Bread",
             "quantity": 1, "purchased": False},
            {"id": str(uuid.uuid4()), "name": "Eggs",
             "quantity": 12, "purchased": True},
            {"id": str(uuid.uuid4()), "name": "Apples",
             "quantity": 6, "purchased": False},
            {"id": str(uuid.uuid4()), "name": "Coffee",
             "quantity": 1, "purchased": False}
        ]

    def get_items(self, purchased=None):
        """Get all items, optionally filtered by completion status."""
        if purchased is None:
            return self.items.copy()

        return [item for item in self.items if item['purchased'] == purchased]

    def add_item(self, name, quantity):
        """Add a new item to the shopping list and return its ID."""
        # Generate a unique ID for the new item
        new_item_id = str(uuid.uuid4())

        # Create the new item as a dictionary
        new_item = {
            'id': new_item_id,
            'name': name,
            'quantity': quantity,
            'purchased': False
        }

        # Add the item to the list
        self.items.append(new_item)

        # Return the ID of the new item
        return new_item_id

    def remove_item(self, item_id):
        """Remove an item from the shopping list by its ID."""
        # Find the index of the item with matching ID
        for index, item in enumerate(self.items):
            if item['id'] == item_id:
                # Remove the item when found
                del self.items[index]
                return True

        # Return False if no item was found with that ID
        return False

    def set_purchased(self, item_id, purchased=True):
        """Mark an item as purchased or not purchased by its ID."""
        # Look for the item with the matching ID
        for item in self.items:
            if item['id'] == item_id:
                # Update the item's purchased status
                item['purchased'] = purchased
                return True

        # Return False if no item was found with that ID
        return False
