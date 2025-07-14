import unittest
import tempfile
import os
import json
from app.models.inventory import Inventory
from app.models.produce import ProduceItem

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()

    def test_add_new_item(self):
        self.inventory.add_item("Tomato", 50, 1.5)
        self.assertEqual(len(self.inventory.produces), 1)
        self.assertEqual(self.inventory.produces[0].name, "Tomato")

    def test_add_existing_item_updates_quantity_and_price(self):
        self.inventory.add_item("Tomato", 50, 1.5)
        self.inventory.add_item("Tomato", 20, 2.0)
        item = self.inventory.produces[0]
        self.assertEqual(item.quantity, 70)
        self.assertEqual(item.price_per_unit, 2.0)

    def test_record_sale_updates_quantity_and_revenue(self):
        self.inventory.add_item("Carrot", 30, 1.0)
        self.inventory.record_sale("Carrot", 10)
        item = self.inventory.produces[0]
        self.assertEqual(item.quantity, 20)
        self.assertAlmostEqual(self.inventory.total_revenue, 10.0)

    def test_record_sale_not_enough_stock(self):
        self.inventory.add_item("Onion", 5, 2.0)
        self.inventory.record_sale("Onion", 10)
        self.assertEqual(self.inventory.total_revenue, 0.0)
        self.assertEqual(self.inventory.produces[0].quantity, 5)

    def test_record_sale_item_not_found(self):
        self.inventory.record_sale("Cabbage", 5)
        self.assertEqual(self.inventory.total_revenue, 0.0)

    def test_get_total_revenue(self):
        self.inventory.add_item("Lettuce", 10, 1.5)
        self.inventory.record_sale("Lettuce", 5)
        self.assertAlmostEqual(self.inventory.get_total_revenue(), 7.5)
        
    def test_save_and_load_inventory_file(self):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            # Step 1: Add item and save
            self.inventory.add_item("Tomato", 10, 1.5)
            self.inventory.record_sale("Tomato", 5)
            self.inventory.save_to_file(temp_path)

            # Step 2: Load into a new Inventory instance
            new_inventory = Inventory()
            new_inventory.load_from_file(temp_path)

            # Step 3: Assertions
            self.assertEqual(len(new_inventory.produces), 1)
            item = new_inventory.produces[0]
            self.assertEqual(item.name, "Tomato")
            self.assertEqual(item.quantity, 5)
            self.assertEqual(item.price_per_unit, 1.5)
            self.assertAlmostEqual(new_inventory.total_revenue, 7.5)

        finally:
            # Clean up the temp file
            os.remove(temp_path)


if __name__ == '__main__':
    unittest.main()
