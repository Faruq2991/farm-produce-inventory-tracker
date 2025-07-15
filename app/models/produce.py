
class ProduceItem():
    def __init__(self, name, quantity, price_per_unit, category, unit_of_measurement):
        """
        Initialize a ProduceItem with name, quantity in stock, and price per unit.
        """
        self.name = name
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.category = category
        self.unit_of_measurement = unit_of_measurement

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
        return f"{self.name} | {self.quantity} | ${self.price_per_unit:.2f} | Category: {self.category} | {self.unit_of_measurement}"
    
    def to_dict(self) -> dict:
        """
        Convert the ProduceItem instance to a dictionary for JSON serialization.
        """
        return {
            "name": self.name,
            "quantity": self.quantity,
            "price_per_unit": self.price_per_unit,
            "category": self.category,
            "unit_of_measurement": self.unit_of_measurement
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Create a ProduceItem instance from a dictionary.
        """
        return ProduceItem(
            name=data["name"],
            quantity=data["quantity"],
            price_per_unit=data["price_per_unit"],
            category=data["category"],
            unit_of_measurement=data["unit_of_measurement"]
        )
