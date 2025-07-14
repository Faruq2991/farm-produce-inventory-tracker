import json
import os
from datetime import datetime
from app.models.produce import ProduceItem

class Inventory():
    def __init__(self):
        self.produces = []
        self.transactions = []
        self.total_revenue = 0.0

    def add_item(self, name: str, quantity: int, price: float):

        for item in self.produces:
            if item.name.lower() == name.lower():
                new_quantity = item.quantity + quantity
                item.update_quantity(new_quantity)
                item.update_price(price)
                print("Updated existing item.")
                return

        produce = ProduceItem(name, quantity, price, category="Uncategorized", unit_of_measurement="unit")
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

    def log_transaction(self, type, produce_name, quantity, price, note=""):
        timestamp = datetime.now().isoformat()
        txn = Transaction(type, produce_name, quantity, price, note, timestamp)
        self.transactions.append(txn)

    def adjust_item(self, name: str, quantity_change: int, note: str = ""):
        for item in self.produces:
            if item.name.lower() == name.lower():
                new_quantity = item.quantity + quantity_change

                if new_quantity < 0:
                    print("❌ Adjustment would result in negative stock. Operation cancelled.")
                    return

                item.update_quantity(new_quantity)

                self.log_transaction(
                type="adjustment",
                produce_name=item.name,
                quantity=abs(quantity_change),
                price=item.price_per_unit,
                note=note
            )

            print(f"✅ Adjustment complete. New quantity for {item.name}: {new_quantity}")
            return
    print("❌ Item not found in inventory.")



    def save_to_file(self, path: str):
        """
        Save the current inventory and total revenue to a JSON file.
        """
        data = {
            "produces": [item.to_dict() for item in self.produces],
            "total_revenue": self.total_revenue,
            "transactions": [txn.to_dict() for txn in self.transactions]
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
            self.transactions = [Transaction.from_dict(txn) for txn in data.get("transactions", [])]

            print(f"✅ Inventory loaded from {path}")
        except Exception as e:
            print(f"❌ Failed to load inventory: {e}")

class Transaction():
    # Valid transaction types
    VALID_TYPES = {"sale", "purchase", "adjustment", "refund"}
    
    def __init__(self, type: str, produce_name: str, quantity: float, unit_price: float, note: str = "", timestamp=None):
        # Validate transaction type
        if type.lower() not in self.VALID_TYPES:
            raise ValueError(f"Invalid transaction type '{type}'. Must be one of: {', '.join(self.VALID_TYPES)}")
        
        self.type = type.lower()  # Store in lowercase for consistency
        self.produce_name = produce_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.note = note

        if timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        else:
            self.timestamp = timestamp


    def __str__(self):
        return f"[{self.timestamp}] {self.type.upper()}: {self.quantity} {self.produce_name} @ ${self.unit_price:.2f} each - {self.note}"

    def to_dict(self) -> dict:
        """
        Convert the Transaction instance to a dictionary for JSON serialization.
        """
        return {
            "type": self.type,
            "produce_name": self.produce_name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "note": self.note,
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Create a Transaction instance from a dictionary.
        """
        return Transaction(
            type=data["type"],
            produce_name=data["produce_name"],
            quantity=data["quantity"],
            unit_price=data["unit_price"],
            note=data["note"],
            timestamp=data["timestamp"]
        )

