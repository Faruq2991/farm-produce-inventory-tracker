import json
import os
from datetime import date, datetime
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
from app.models.produce import ProduceItem
from app.models.transaction import Transaction


class InventoryError(Exception):
    """Custom exception for inventory-related errors."""
    pass


class Inventory:
    """
    Enhanced inventory management system for produce items.
    
    Features:
    - Add, update, and adjust inventory items
    - Record sales and track revenue
    - Transaction logging with filtering
    - Low stock alerts
    - Data persistence (JSON)
    - Inventory valuation and reporting
    """
    
    def __init__(self):
        self.produces: List[ProduceItem] = []
        self.transactions: List[Transaction] = []
        self._total_revenue = Decimal('0.00')

    def add_item(self, name: str, quantity: int, price: float, 
                 category: str = "Uncategorized", unit: str = "unit") -> bool:
        """
        Add a new item to inventory or update existing item.
        
        Args:
            name: Item name
            quantity: Quantity to add
            price: Price per unit
            category: Item category
            unit: Unit of measurement
            
        Returns:
            bool: True if item was added/updated successfully
        """
        if quantity < 0:
            raise InventoryError("Quantity cannot be negative")
        if price < 0:
            raise InventoryError("Price cannot be negative")
        
        name = name.strip()
        if not name:
            raise InventoryError("Item name cannot be empty")

        # Check if item already exists
        existing_item = self._find_item_by_name(name)
        if existing_item:
            new_quantity = existing_item.quantity + quantity
            existing_item.update_quantity(new_quantity)
            existing_item.update_price(price)
            
            # Log the transaction
            self._log_transaction(
                type="purchase",
                produce_name=name,
                quantity=quantity,
                price=Decimal(str(price)),
                note=f"Restocked existing item"
            )
            
            print(f"✅ Updated existing item: {name}")
            return True

        # Create new item
        produce = ProduceItem(name, quantity, price, category, unit)
        self.produces.append(produce)
        
        # Log the transaction
        self._log_transaction(
            type="purchase",
            produce_name=name,
            quantity=quantity,
            price=Decimal(str(price)),
            note=f"Added new item to inventory"
        )
        
        print(f"✅ New item added to inventory: {name}")
        return True

    def remove_item(self, name: str) -> bool:
        """Remove an item completely from inventory."""
        item = self._find_item_by_name(name)
        if not item:
            print(f"❌ Item '{name}' not found in inventory")
            return False
        
        self.produces.remove(item)
        self._log_transaction(
            type="adjustment",
            produce_name=name,
            quantity=item.quantity,
            price=Decimal(str(item.price_per_unit)),
            note="Item removed from inventory"
        )
        
        print(f"✅ Item '{name}' removed from inventory")
        return True

    def list_items(self, category: Optional[str] = None, 
                   show_low_stock: bool = False, threshold: int = 10) -> None:
        """
        List inventory items with optional filtering.
        
        Args:
            category: Filter by category (optional)
            show_low_stock: Show only low stock items
            threshold: Low stock threshold
        """
        if not self.produces:
            print("📦 Inventory is empty.")
            return

        items_to_show = self.produces
        
        if category:
            items_to_show = [item for item in items_to_show 
                           if item.category.lower() == category.lower()]
        
        if show_low_stock:
            items_to_show = [item for item in items_to_show 
                           if item.quantity <= threshold]

        if not items_to_show:
            filter_desc = f" (Category: {category})" if category else ""
            filter_desc += " (Low stock only)" if show_low_stock else ""
            print(f"📦 No items found{filter_desc}.")
            return

        print("\n📋 Current Inventory:")
        print("-" * 0)
        for item in sorted(items_to_show, key=lambda x: x.name):
            stock_status = "⚠️ LOW" if item.quantity <= threshold else "✅"
            print(f"{stock_status} {item}")

    def record_sale(self, name: str, quantity_sold: int, 
                   customer_note: str = "") -> bool:
        """
        Record a sale transaction.
        
        Args:
            name: Item name
            quantity_sold: Quantity sold
            customer_note: Optional note about the sale
            
        Returns:
            bool: True if sale was recorded successfully
        """
        if quantity_sold <= 0:
            raise InventoryError("Quantity sold must be positive")

        item = self._find_item_by_name(name)
        if not item:
            print(f"❌ Item '{name}' not found in inventory")
            return False

        if quantity_sold > item.quantity:
            print(f"❌ Not enough stock available. Current stock: {item.quantity}")
            return False

        # Update inventory
        new_quantity = item.quantity - quantity_sold
        item.update_quantity(new_quantity)
        
        # Calculate sale amount
        sale_amount = Decimal(str(quantity_sold)) * Decimal(str(item.price_per_unit))
        self._total_revenue += sale_amount

        # Log the transaction
        self._log_transaction(
            type="sale",
            produce_name=name,
            quantity=quantity_sold,
            price=Decimal(str(item.price_per_unit)),
            note=customer_note
        )

        print(f"✅ Sale recorded: {quantity_sold} {item.name} sold for ${sale_amount:.2f}")
        
        # Check for low stock
        if new_quantity <= 10:  # Default threshold
            print(f"⚠️ Low stock alert: {item.name} has only {new_quantity} units left")
        
        return True

    def adjust_item(self, name: str, quantity_change: int, note: str = "") -> bool:
        """
        Adjust item quantity (for spoilage, damage, etc.).
        
        Args:
            name: Item name
            quantity_change: Change in quantity (can be negative)
            note: Reason for adjustment
            
        Returns:
            bool: True if adjustment was successful
        """
        item = self._find_item_by_name(name)
        if not item:
            print(f"❌ Item '{name}' not found in inventory")
            return False

        new_quantity = item.quantity + quantity_change

        if new_quantity < 0:
            print(f"❌ Adjustment would result in negative stock. Current: {item.quantity}")
            return False

        item.update_quantity(new_quantity)

        self._log_transaction(
            type="adjustment",
            produce_name=item.name,
            quantity=abs(quantity_change),
            price=Decimal(str(item.price_per_unit)),
            note=note or ("Stock increase" if quantity_change > 0 else "Stock decrease")
        )

        adjustment_type = "increased" if quantity_change > 0 else "decreased"
        print(f"✅ Adjustment complete: {item.name} {adjustment_type} by {abs(quantity_change)} units. New quantity: {new_quantity}")
        return True

    def get_total_revenue(self) -> Decimal:
        """Get total revenue from all sales."""
        return self._total_revenue

    def check_low_stock(self, threshold: int = 10) -> List[ProduceItem]:
        """
        Get list of items with low stock.
        
        Args:
            threshold: Stock level threshold
            
        Returns:
            List of items with stock <= threshold
        """
        return [item for item in self.produces if item.quantity <= threshold]

    def get_transaction_history(self) -> List['Transaction']:
        """Get all transactions."""
        return self.transactions.copy()

    def filter_transactions_by_type(self, transaction_type: str) -> List['Transaction']:
        """Filter transactions by type."""
        return [tx for tx in self.transactions 
                if tx.type.lower() == transaction_type.lower()]

    def filter_transactions_by_date(self, start: date, end: date) -> List['Transaction']:
        """Filter transactions by date range."""
        results = []
        for txn in self.transactions:
            txn_datetime = datetime.fromisoformat(txn.timestamp)
            txn_date = txn_datetime.date()

            if start <= txn_date <= end:
                results.append(txn)
        return results

    def get_inventory_value(self) -> Tuple[Decimal, List[Dict]]:
        """
        Calculate total inventory value and breakdown.
        
        Returns:
            Tuple of (total_value, breakdown_list)
        """
        total_value = Decimal('0.00')
        breakdown = []
        
        for item in self.produces:
            item_value = Decimal(str(item.quantity)) * Decimal(str(item.price_per_unit))
            total_value += item_value
            breakdown.append({
                "name": item.name,
                "quantity": item.quantity,
                "price": float(item.price_per_unit),
                "value": float(item_value),
                "category": item.category
            })

        return total_value, breakdown

    def get_inventory_report(self) -> Dict:
        """Generate comprehensive inventory report."""
        total_value, breakdown = self.get_inventory_value()
        low_stock_items = self.check_low_stock()
        
        # Category breakdown
        categories = {}
        for item in self.produces:
            cat = item.category
            if cat not in categories:
                categories[cat] = {"items": 0, "total_value": Decimal('0.00')}
            categories[cat]["items"] += 1
            categories[cat]["total_value"] += Decimal(str(item.quantity)) * Decimal(str(item.price_per_unit))

        return {
            "total_items": len(self.produces),
            "total_value": float(total_value),
            "total_revenue": float(self._total_revenue),
            "low_stock_items": len(low_stock_items),
            "categories": {k: {"items": v["items"], "total_value": float(v["total_value"])} 
                         for k, v in categories.items()},
            "recent_transactions": len([tx for tx in self.transactions 
                                     if (datetime.now() - datetime.fromisoformat(tx.timestamp)).days <= 7])
        }

    def _find_item_by_name(self, name: str) -> Optional[ProduceItem]:
        """Find item by name (case-insensitive)."""
        name_lower = name.lower().strip()
        for item in self.produces:
            if item.name.lower() == name_lower:
                return item
        return None

    def _log_transaction(self, type: str, produce_name: str, quantity: int, 
                        price: Decimal, note: str = "") -> None:
        """Log a transaction."""
        txn = Transaction(type, produce_name, quantity, float(price), note)
        self.transactions.append(txn)

    def export_inventory_to_csv(self, filepath: str):
        """
        Export inventory data to CSV file.
        
        Args:
            filepath: Path to save the CSV file
            
        Returns:
            bool: True if export was successful
        """
        if not self.produces:
            print("❌ No inventory data to export")
            return False
        try:
            data = []
            for produce in self.produces:
                produce_dict = produce.to_dict()
                produce_dict['total_value'] = float(
                        Decimal(str(produce_dict['quantity'])) * Decimal(str(produce_dict['price_per_unit'])))
                data.append(produce_dict)
            success = self._export_to_csv(data, filepath)
            if success:
                print(f"✅ Inventory exported to {filepath}")
            return success
        except Exception as e:
            print(f"❌ Failed to export inventory: {e}")
            return False

    def export_transactions_to_csv(self, filepath: str):
        """
        Export transaction history to CSV file.
        
        Args:
            filepath: Path to save the CSV file
            
        Returns:
            bool: True if export was successful
        """
        if not self.produces:
            print("❌ No transaction data to export")
            return False
        try:
            data = []
            for txn in self.transactions:
                txn_dict = txn.to_dict()
                txn_dict['total_amount'] = float(txn.total_amount)
                txn_dict['formatted_date'] = datetime.fromisoformat(txn.timestamp).strftime('%Y-%m-%d %H:%M:%S')
                data.append(txn_dict)
            success = self._export_to_csv(data, filepath)
            if success:
                print(f"✅ Transactions exported to {filepath}")
            return success
        except Exception as e:
            print(f"❌ Failed to export transactions: {e}")
            return False

    def export_full_report_to_csv(self, filepath: str) -> bool:
        """
        Export a comprehensive report to CSV file.
        
        Args:
            filepath: Path to save the CSV file
            
        Returns:
            bool: True if export was successful
        """
        try:
            report = self.get_inventory_report()
            total_value, breakdown = self.get_inventory_value()
            
            data = []
            for item in breakdown:
                # Combine inventory and report data
                item_data = {
                    'item_name': item['name'],
                    'quantity': item['quantity'],
                    'price_per_unit': item['price'],
                    'total_value': item['value'],
                    'category': item['category'],
                    'stock_status': 'Low Stock' if item['quantity'] <= 10 else 'Normal'
                }
                data.append(item_data)
            
            # Add summary row
            summary_row = {
                'item_name': 'SUMMARY',
                'quantity': report['total_items'],
                'price_per_unit': 0,
                'total_value': report['total_value'],
                'category': f"Total Revenue: ${report['total_revenue']:.2f}",
                'stock_status': f"Low Stock Items: {report['low_stock_items']}"
            }
            data.append(summary_row)
            
            success = self._export_to_csv(data, filepath)
            if success:
                print(f"✅ Full report exported to {filepath}")
            return success
            
        except Exception as e:
            print(f"❌ Failed to export report: {e}")
            return False

    def _export_to_csv(self, data: List[Dict], filepath: str) -> bool:
        """
        Export data to CSV file using Python's built-in csv module.
        
        Args:
            data: List of dictionaries to export
            filepath: Path to save the CSV file
            
        Returns:
            bool: True if export was successful
        """
        import csv
        
        if not data:
            print("❌ No data to export")
            return False
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Get all possible field names from the data
            fieldnames = set()
            for item in data:
                fieldnames.update(item.keys())
            fieldnames = sorted(list(fieldnames))
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            return True
            
        except Exception as e:
            print(f"❌ CSV export failed: {e}")
            return False

    def save_to_file(self, path: str) -> bool:
        """
        Save inventory data to JSON file.
        
        Args:
            path: File path to save to
            
        Returns:
            bool: True if saved successfully
        """
        data = {
            "produces": [item.to_dict() for item in self.produces],
            "total_revenue": str(self._total_revenue),
            "transactions": [txn.to_dict() for txn in self.transactions],
            "last_updated": datetime.now().isoformat()
        }

        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as file:
                json.dump(data, file, indent=2)
            print(f"✅ Inventory saved to {path}")
            return True
        except Exception as e:
            print(f"❌ Failed to save inventory: {e}")
            return False
      

    def load_from_file(self, path: str) -> bool:
        """
        Load inventory data from JSON file.
        
        Args:
            path: File path to load from
            
        Returns:
            bool: True if loaded successfully
        """
        if not os.path.exists(path):
            print(f"📁 No saved inventory found at {path}. Starting fresh.")
            return False

        try:
            with open(path, "r") as file:
                data = json.load(file)

            self.produces = [ProduceItem.from_dict(item) for item in data.get("produces", [])]
            self._total_revenue = Decimal(data.get("total_revenue", "0.00"))
            self.transactions = [Transaction.from_dict(txn) for txn in data.get("transactions", [])]

            print(f"✅ Inventory loaded from {path}")
            return True
        except Exception as e:
            print(f"❌ Failed to load inventory: {e}")
            return False
