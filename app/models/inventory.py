
from app.models.produce import ProduceItem

class Inventory():
    def __init__(self):
        self.produces = []
        self.total_revenue = 0.0
        return

    def add_item(self, name: str, quantity: int, price: float):
        produce = ProduceItem(name, quantity, price)
        self.produces.append(produce)

        for item in self.produces:
            if item.name.lower() == item.lower():
                produce.update_quantity(item.quantity + quantity)
                produce.update_price(price)
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

        return

    def get_total_revenue(self):
        return
