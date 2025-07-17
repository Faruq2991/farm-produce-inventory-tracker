import sys
import os
from datetime import datetime, date
from typing import Optional
from app.models.inventory import Inventory, InventoryError


class InventoryCLI:
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.inventory = Inventory()
        self.inventory.load_from_file(file_path)
        self.running = True
        
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("🌽 Farm Produce Inventory Tracker 🌽")
        print("="*50)
        print("1. 📦 Add a new produce item")
        print("2. 📋 View all produce in stock")
        print("3. 💰 Record a sale")
        print("4. 📊 View total revenue")
        print("5. ⚙️  Adjust item quantity")
        print("6. 📑 View Reports")
        print("7. 🔧 Advanced Options")
        print("8. 💾 Save and Exit")
        print("="*50)
    
    def display_reports_menu(self):
        """Display the reports submenu."""
        print("\n" + "="*40)
        print("📊 REPORTS MENU")
        print("="*40)
        print("1. 📄 View all transactions")
        print("2. 💎 Inventory value summary")
        print("3. ⚠️  Low stock items")
        print("4. 🔍 Filter transactions by type")
        print("5. 📅 Filter transactions by date")
        print("6. 📈 Comprehensive inventory report")
        print("0. ← Back to Main Menu")
        print("="*40)
    
    def display_advanced_menu(self):
        """Display the advanced options menu."""
        print("\n" + "="*40)
        print("🔧 ADVANCED OPTIONS")
        print("="*40)
        print("1. 🗑️  Remove item from inventory")
        print("2. 📦 View items by category")
        print("3. 💾 Save inventory manually")
        print("4. 🔄 Reload inventory from file")
        print("5. 📊 Export transaction history (TXT)")
        print("6. 📈 Export inventory to CSV")
        print("7. 📋 Export transactions to CSV")
        print("8. 📄 Export full report to CSV")
        print("0. ← Back to Main Menu")
        print("="*40)
    
    def get_user_choice(self, prompt: str, valid_range: range) -> int:
        """Get and validate user choice."""
        while True:
            try:
                choice = input(prompt).strip()
                if not choice.isdigit():
                    raise ValueError("Please enter a number")
                
                choice_int = int(choice)
                if choice_int not in valid_range:
                    raise ValueError(f"Please enter a number between {valid_range.start} and {valid_range.stop-1}")
                
                return choice_int
            except ValueError as e:
                print(f"❌ Invalid input: {e}")
    
    def get_positive_int(self, prompt: str) -> int:
        """Get a positive integer from user."""
        while True:
            try:
                value = int(input(prompt).strip())
                if value <= 0:
                    raise ValueError("Must be a positive number")
                return value
            except ValueError as e:
                print(f"❌ Invalid input: {e if 'invalid literal' not in str(e) else 'Please enter a valid positive number'}")
    
    def get_positive_float(self, prompt: str) -> float:
        """Get a positive float from user."""
        while True:
            try:
                value = float(input(prompt).strip())
                if value < 0:
                    raise ValueError("Must be non-negative")
                return value
            except ValueError as e:
                print(f"❌ Invalid input: {e if 'could not convert' not in str(e) else 'Please enter a valid number'}")
    
    def get_date_input(self, prompt: str) -> date:
        """Get a date from user input."""
        while True:
            try:
                date_str = input(prompt + " (YYYY-MM-DD): ").strip()
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print("❌ Invalid date format. Please use YYYY-MM-DD (e.g., 2024-01-15)")
    
    def show_low_stock_alert(self):
        """Show low stock alert if any items are running low."""
        low_stock_items = self.inventory.check_low_stock()
        if low_stock_items:
            print("\n⚠️  LOW STOCK ALERT:")
            print("-" * 30)
            for item in low_stock_items:
                print(f"   • {item.name}: Only {item.quantity} {item.unit_of_measurement} left")
            print("-" * 30)
    
    def handle_add_item(self):
        """Handle adding a new item to inventory."""
        print("\n➕ ADD NEW PRODUCE ITEM")
        print("-" * 30)
        
        name = input("Enter produce name: ").strip()
        if not name:
            print("❌ Item name cannot be empty")
            return
        
        qty = self.get_positive_int("Enter quantity: ")
        price = self.get_positive_float("Enter price per unit: $")
        
        # Optional fields
        category = input("Enter category (optional, press Enter for 'Uncategorized'): ").strip()
        if not category:
            category = "Uncategorized"
        
        unit = input("Enter unit of measurement (optional, press Enter for 'unit'): ").strip()
        if not unit:
            unit = "unit"
        
        try:
            self.inventory.add_item(name, qty, price, category, unit)
            self.show_low_stock_alert()
        except InventoryError as e:
            print(f"❌ Error: {e}")
    
    def handle_record_sale(self):
        """Handle recording a sale."""
        print("\n💰 RECORD SALE")
        print("-" * 20)
        
        name = input("Enter item name: ").strip()
        if not name:
            print("❌ Item name cannot be empty")
            return
        
        qty = self.get_positive_int("Enter quantity sold: ")
        note = input("Enter customer note (optional): ").strip()
        
        try:
            success = self.inventory.record_sale(name, qty, note)
            if success:
                self.show_low_stock_alert()
        except InventoryError as e:
            print(f"❌ Error: {e}")
    
    def handle_adjust_item(self):
        """Handle adjusting item quantity."""
        print("\n⚙️ ADJUST ITEM QUANTITY")
        print("-" * 30)
        
        name = input("Enter item name: ").strip()
        if not name:
            print("❌ Item name cannot be empty")
            return
        
        print("Enter quantity change:")
        print("  • Positive number to increase stock")
        print("  • Negative number to decrease stock")
        
        while True:
            try:
                qty_change = int(input("Quantity change: ").strip())
                if qty_change == 0:
                    print("❌ Change cannot be zero")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid integer")
        
        note = input("Reason for adjustment (optional): ").strip()
        
        try:
            success = self.inventory.adjust_item(name, qty_change, note)
            if success:
                self.show_low_stock_alert()
        except InventoryError as e:
            print(f"❌ Error: {e}")
    
    def handle_view_transactions(self):
        """Handle viewing transaction history."""
        transactions = self.inventory.get_transaction_history()
        if not transactions:
            print("📄 No transactions found")
            return
        
        print(f"\n📄 TRANSACTION HISTORY ({len(transactions)} transactions)")
        print("-" * 80)
        for txn in transactions[-20:]:  # Show last 20 transactions
            print(f"  {txn}")
        
        if len(transactions) > 20:
            print(f"\n... showing last 20 of {len(transactions)} transactions")
    
    def handle_inventory_value(self):
        """Handle showing inventory value summary."""
        total_value, breakdown = self.inventory.get_inventory_value()
        
        print(f"\n💎 INVENTORY VALUE SUMMARY")
        print("-" * 50)
        print(f"Total Inventory Value: ${total_value:.2f}")
        print(f"Total Revenue to Date: ${self.inventory.get_total_revenue():.2f}")
        print("\nBreakdown by item:")
        
        for item in sorted(breakdown, key=lambda x: x['value'], reverse=True):
            print(f"  • {item['name']}: {item['quantity']} @ ${item['price']:.2f} = ${item['value']:.2f}")
    
    def handle_low_stock_report(self):
        """Handle showing low stock report."""
        threshold = self.get_positive_int("Enter stock threshold (default 10): ")
        low_stock_items = self.inventory.check_low_stock(threshold)
        
        if not low_stock_items:
            print(f"✅ No items below {threshold} units")
            return
        
        print(f"\n⚠️  LOW STOCK REPORT (threshold: {threshold})")
        print("-" * 40)
        for item in low_stock_items:
            print(f"  • {item.name}: {item.quantity} {item.unit_of_measurement} (${item.price_per_unit:.2f}/unit)")
    
    def handle_filter_transactions_by_type(self):
        """Handle filtering transactions by type."""
        print("\nAvailable transaction types:")
        print("  • sale")
        print("  • purchase") 
        print("  • adjustment")
        print("  • refund")
        
        txn_type = input("Enter transaction type: ").strip()
        filtered = self.inventory.filter_transactions_by_type(txn_type)
        
        if not filtered:
            print(f"📄 No {txn_type} transactions found")
            return
        
        print(f"\n📄 {txn_type.upper()} TRANSACTIONS ({len(filtered)} found)")
        print("-" * 60)
        for txn in filtered:
            print(f"  {txn}")
    
    def handle_filter_transactions_by_date(self):
        """Handle filtering transactions by date range."""
        print("\n📅 FILTER TRANSACTIONS BY DATE")
        print("-" * 40)
        
        start_date = self.get_date_input("Enter start date")
        end_date = self.get_date_input("Enter end date")
        
        if start_date > end_date:
            print("❌ Start date must be before end date")
            return
        
        filtered = self.inventory.filter_transactions_by_date(start_date, end_date)
        
        if not filtered:
            print(f"📄 No transactions found between {start_date} and {end_date}")
            return
        
        print(f"\n📄 TRANSACTIONS FROM {start_date} TO {end_date} ({len(filtered)} found)")
        print("-" * 70)
        for txn in filtered:
            print(f"  {txn}")
    
    def handle_comprehensive_report(self):
        """Handle showing comprehensive inventory report."""
        report = self.inventory.get_inventory_report()
        
        print(f"\n📈 COMPREHENSIVE INVENTORY REPORT")
        print("=" * 50)
        print(f"Total Items: {report['total_items']}")
        print(f"Total Inventory Value: ${report['total_value']:.2f}")
        print(f"Total Revenue: ${report['total_revenue']:.2f}")
        print(f"Low Stock Items: {report['low_stock_items']}")
        print(f"Recent Transactions (7 days): {report['recent_transactions']}")
        
        print(f"\nCategories:")
        for cat, data in report['categories'].items():
            print(f"  • {cat}: {data['items']} items, ${data['total_value']:.2f}")
    
    def handle_remove_item(self):
        """Handle removing an item from inventory."""
        print("\n🗑️ REMOVE ITEM FROM INVENTORY")
        print("-" * 40)
        
        name = input("Enter item name to remove: ").strip()
        if not name:
            print("❌ Item name cannot be empty")
            return
        
        # Show item details before removal
        item = self.inventory._find_item_by_name(name)
        if not item:
            print(f"❌ Item '{name}' not found")
            return
        
        print(f"Item to remove: {item}")
        confirm = input("Are you sure you want to remove this item? (y/N): ").strip().lower()
        
        if confirm == 'y':
            self.inventory.remove_item(name)
        else:
            print("❌ Removal cancelled")
    
    def handle_view_by_category(self):
        """Handle viewing items by category."""
        print("\n📦 VIEW ITEMS BY CATEGORY")
        print("-" * 40)
        
        category = input("Enter category name (or press Enter for all): ").strip()
        show_low_stock = input("Show only low stock items? (y/N): ").strip().lower() == 'y'
        
        if category:
            self.inventory.list_items(category=category, show_low_stock=show_low_stock)
        else:
            self.inventory.list_items(show_low_stock=show_low_stock)
    
    def handle_export_transactions(self):
        """Handle exporting transaction history to text file."""
        transactions = self.inventory.get_transaction_history()
        if not transactions:
            print("📄 No transactions to export")
            return
        
        filename = f"transactions_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("TRANSACTION HISTORY EXPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                for txn in transactions:
                    f.write(f"{txn}\n")
            
            print(f"✅ Transactions exported to {filename}")
        except Exception as e:
            print(f"❌ Export failed: {e}")

    def handle_export_inventory_csv(self):
        """Handle exporting inventory to CSV file."""
        print("\n📈 EXPORT INVENTORY TO CSV")
        print("-" * 40)
        
        filename = input("Enter filename (press Enter for auto-generated): ").strip()
        if not filename:
            filename = f"inventory_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        success = self.inventory.export_inventory_to_csv(filename)
        if success:
            print(f"📊 Inventory data exported with {len(self.inventory.produces)} items")

    def handle_export_transactions_csv(self):
        """Handle exporting transactions to CSV file."""
        print("\n📋 EXPORT TRANSACTIONS TO CSV")
        print("-" * 40)
        
        filename = input("Enter filename (press Enter for auto-generated): ").strip()
        if not filename:
            filename = f"transactions_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        success = self.inventory.export_transactions_to_csv(filename)
        if success:
            print(f"📊 Transaction data exported with {len(self.inventory.transactions)} records")

    def handle_export_full_report_csv(self):
        """Handle exporting full report to CSV file."""
        print("\n📄 EXPORT FULL REPORT TO CSV")
        print("-" * 40)
        
        filename = input("Enter filename (press Enter for auto-generated): ").strip()
        if not filename:
            filename = f"full_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        success = self.inventory.export_full_report_to_csv(filename)
        if success:
            print("📊 Full report exported with inventory summary and details")
    
    def handle_reports_menu(self):
        """Handle the reports submenu."""
        while True:
            self.display_reports_menu()
            choice = self.get_user_choice("Select report option: ", range(0, 7))
            
            if choice == 0:
                break
            elif choice == 1:
                self.handle_view_transactions()
            elif choice == 2:
                self.handle_inventory_value()
            elif choice == 3:
                self.handle_low_stock_report()
            elif choice == 4:
                self.handle_filter_transactions_by_type()
            elif choice == 5:
                self.handle_filter_transactions_by_date()
            elif choice == 6:
                self.handle_comprehensive_report()
            
            input("\nPress Enter to continue...")
    
    def handle_advanced_menu(self):
        """Handle the advanced options submenu."""
        while True:
            self.display_advanced_menu()
            choice = self.get_user_choice("Select advanced option: ", range(0, 9))
            
            if choice == 0:
                break
            elif choice == 1:
                self.handle_remove_item()
            elif choice == 2:
                self.handle_view_by_category()
            elif choice == 3:
                print("💾 Saving inventory...")
                success = self.inventory.save_to_file(self.file_path)
                if success:
                    print("✅ Inventory saved successfully")
            elif choice == 4:
                print("🔄 Reloading inventory...")
                success = self.inventory.load_from_file(self.file_path)
                if success:
                    print("✅ Inventory reloaded successfully")
            elif choice == 5:
                self.handle_export_transactions()
            elif choice == 6:
                self.handle_export_inventory_csv()
            elif choice == 7:
                self.handle_export_transactions_csv()
            elif choice == 8:
                self.handle_export_full_report_csv()
            
            input("\nPress Enter to continue...")
    
    def run(self):
        """Run the main CLI loop."""
        print("🌟 Welcome to Farm Produce Inventory Tracker!")
        print(f"📁 Using data file: {self.file_path}")
        
        # Show initial low stock alert
        self.show_low_stock_alert()
        
        while self.running:
            try:
                self.display_menu()
                choice = self.get_user_choice("Select option (1-8): ", range(1, 9))
                
                if choice == 1:
                    self.handle_add_item()
                elif choice == 2:
                    print("\n📦 CURRENT INVENTORY:")
                    self.inventory.list_items()
                elif choice == 3:
                    self.handle_record_sale()
                elif choice == 4:
                    revenue = self.inventory.get_total_revenue()
                    print(f"\n💰 Total Revenue: ${revenue:.2f}")
                elif choice == 5:
                    self.handle_adjust_item()
                elif choice == 6:
                    self.handle_reports_menu()
                elif choice == 7:
                    self.handle_advanced_menu()
                elif choice == 8:
                    self.running = False
                
                if choice != 6 and choice != 7 and choice != 8:  # Don't pause for submenus
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️ Interrupted by user")
                self.running = False
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                input("Press Enter to continue...")
        
        # Save before exiting
        print("\n💾 Saving inventory before exit...")
        success = self.inventory.save_to_file(self.file_path)
        if success:
            print("✅ Inventory saved successfully")
        
        print("👋 Thank you for using Farm Produce Inventory Tracker!")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("❌ Please provide a file path to store your inventory.")
        print("Usage: python main.py data/inventory.json")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Create directory if it doesn't exist
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        sys.exit(1)
    
    # Initialize and run CLI
    cli = InventoryCLI(file_path)
    cli.run()


if __name__ == "__main__":
    main()