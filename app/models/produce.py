

class ProduceItem():
    def __init__(self, name, quantity, price_per_unit):
        """
        Initialize a ProduceItem with name, quantity in stock, and price per unit.
        """
        self.name = name
        self.quantity = quantity
        self.price_per_unit = price_per_unit

    def update_quantity(self, new_quantity: int):
        if new_quantity >= 0:
            self.quantity = new_quantity
        else: 
            raise ValueError("Quantity cannot be negative.")

    def update_price(self, new_price: float):
        if new_price >= 0:
            self.price_per_unit = new_price
        else:
            raise ValueError("Price cannot be negative.")

    def __str__(self) -> str:
        return f"{self.name} | {self.quantity} | ${self.price_per_unit:.2f} each"
        