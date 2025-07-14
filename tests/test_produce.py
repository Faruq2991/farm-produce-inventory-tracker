
import unittest
from app.models.produce import ProduceItem

class TestProduceItem(unittest.TestCase):

    def test_initialization(self):
        item = ProduceItem("Tomato", 100, 1.5)
        self.assertEqual(item.name, "Tomato")
        self.assertEqual(item.quantity, 100)
        self.assertEqual(item.price_per_unit, 1.5)

    def test_update_quantity(self):
        item = ProduceItem("Carrot", 50, 2.0)
        item.update_quantity(80)
        self.assertEqual(item.quantity, 80)

    def test_update_price(self):
        item = ProduceItem("Carrot", 50, 2.0)
        item.update_price(2.5)
        self.assertEqual(item.price_per_unit, 2.5)

    def test_to_dict(self):
        item = ProduceItem("Pepper", 20, 0.75)
        expected = {"name": "Pepper", "quantity": 20, "price_per_unit": 0.75}
        self.assertEqual(item.to_dict(), expected)

    def test_from_dict(self):
        data = {"name": "Onion", "quantity": 40, "price_per_unit": 1.0}
        item = ProduceItem.from_dict(data)
        self.assertEqual(item.name, "Onion")
        self.assertEqual(item.quantity, 40)
        self.assertEqual(item.price_per_unit, 1.0)

if __name__ == '__main__':
    unittest.main()
