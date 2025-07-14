import json
import os
from app.models.produce import ProduceItem

class Inventory():
    def __init__(self):
        self.produces = []
        self.total_revenue = 0.0

    def add_item(self, name: str, quantity: int, price: float):

        for item in self.produces:
            if item.name.lower() == item.lower():
                new_quantity = item.quantity + quantity
                item.update_quantity(new_quantity)
                item.update_price(price)
                print("Updated existing item.")
                return

        produce = ProduceItem(name, quantity, price)
        self.produces.append(produce)
        print("New item added to inventory.")

    def list_items(self):
        if not self.produces:
            print("Inventory is empty.")
        else:
            for item in self.produces:
                print(item)

    def record_sale(self, name: str, quantity_sold: int):
        for item in self.produces:
            if item.name.lower() == name.lower():
                if quantity_sold > item.quantity:
                    print("Not enough stock available.")
                    return
                new_quantity = item.quantity - quantity_sold
                item.update_quantity(new_quantity)
                sale_amount = quantity_sold * item.price_per_unit
                self.total_revenue += sale_amount

                print(f"{quantity_sold} {item.name} sold for ${sale_amount:.2f}")
                return
        print("Item not found in inventory.")
        return

    def get_total_revenue(self):
        return self.total_revenue

    def save_to_file(self, path: str):
        """
        Save the current inventory and total revenue to a JSON file.
        """
        data = {
            "produces": [item.to_dict() for item in self.produces],
            "total_revenue": self.total_revenue
        }

        # Ensure the parent directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        try:
            with open(path, "w") as file:
                json.dump(data, file, indent=4)
            print(f"✅ Inventory saved to {path}")
        except Exception as e:
            print(f"❌ Failed to save inventory: {e}")

    def load_from_file(self, path: str):
        """
        Load inventory and revenue from a JSON file if it exists.
        """
        if not os.path.exists(path):
            print(f"📁 No saved inventory found at {path}. Starting fresh.")
            return

        try:
            with open(path, "r") as file:
                data = json.load(file)

            self.produces = [ProduceItem.from_dict(item) for item in data.get("produces", [])]
            self.total_revenue = data.get("total_revenue", 0.0)

            print(f"✅ Inventory loaded from {path}")
        except Exception as e:
            print(f"❌ Failed to load inventory: {e}")
