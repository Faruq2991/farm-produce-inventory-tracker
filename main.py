from datetime import date
import sys
import os
from datetime import datetime
from app.models.inventory import Inventory

if len(sys.argv) < 2:
    print("❌ Please provide a file path to store your inventory.")
    print("Usage: python main.py data/inventory.json")
    sys.exit(1)

file_path = sys.argv[1]

inventory: Inventory = Inventory()
inventory.load_from_file(file_path)

def display_menu():
    print("\n🌽 Farm Produce Inventory Tracker 🌽")
    print("1. Add a new produce item")
    print("2. View all produce in stock")
    print("3. Record a sale")
    print("4. View total revenue")
    print("5. Adjust item quantity")
    print("6. View Reports")
    print("7. Exit")

def reports_menu():
    print("\nView Reports")
    print("1. 📄 View all transactions")
    print("2. 💰 View total revenue")
    print("3. 📦 Inventory value summary")
    print("4. ⚠️ Low stock items")
    print("5. 🔍 Filter transactions by type")
    print("7. 📅 Filter transactions by date")
    print("0. Back to Main Menu")

while True:
    display_menu()
    choice_input = input("Select an option (1–7): ").strip()
    
    if not choice_input.isdigit() or int(choice_input) not in range(1, 8):
        print("❌ Invalid choice. Please enter a number from 1 to 7")
        continue
    
    choice = int(choice_input)

    if choice == 1:
        name = input("Enter Produce name: ").strip()

        try:
            qty = int(input("Enter QTY: "))
            if qty <= 0:
                raise ValueError("Quantity must be a positive number.")
        except ValueError:
            print("❌ Invalid quantity. Please enter a positive integer.")
            continue

        try:
            price = float(input("Enter Price Per Unit: "))
            if price < 0:
                raise ValueError("Price must be non-negative.")
        except ValueError:
            print("❌ Invalid price. Please enter a valid number.")
            continue

        inventory.add_item(name, qty, price)
        print(f"✅ '{qty}' of {name} added to your inventory!")

        # 🟡 Low-stock check
        low_stock_items = inventory.check_low_stock()
        if low_stock_items:
            print("\n⚠️  Low Stock Alert:")
            for item in low_stock_items:
                print(f" - {item.name}: Only {item.quantity} left")

    elif choice == 2:
        print("\n📦 Current Inventory:")
        inventory.list_items()

    elif choice == 3:
        name = input("Stock name: ").strip()
        try:
            qty = int(input("Qty Sold: "))
            if qty <= 0:
                raise ValueError
        except ValueError:
            print("❌ Invalid quantity. Enter a positive whole number.")
            continue

        inventory.record_sale(name, qty)

        # 🟡 Low-stock check
        low_stock_items = inventory.check_low_stock()
        if low_stock_items:
            print("\n⚠️  Low Stock Alert:")
            for item in low_stock_items:
                print(f" - {item.name}: Only {item.quantity} left")

    elif choice == 4:
        sales = inventory.get_total_revenue()
        print(f"💰 Total Revenue: ${sales:.2f}")

    elif choice == 5:
        name = input("Enter item to adjust: ").strip()
        try:
            qty_change = int(input("Enter quantity change (use negative for decrease): "))
            if qty_change == 0:
                raise ValueError("Zero is not a valid adjustment.")

            note = input("Reason for adjustment (optional): ").strip()
            
            # Check if adjust_item method exists, if not, provide alternative
            if hasattr(inventory, 'adjust_item'):
                inventory.adjust_item(name, qty_change, note)
            else:
                print("❌ Adjust item functionality not yet implemented.")
                print("💡 You can manually add/remove items using options 1 and 3.")
        except ValueError:
            print("❌ Quantity change must be a valid integer.")

        low_stock_items = inventory.check_low_stock()
        if low_stock_items:
            print("\n⚠️  Low Stock Alert:")
            for item in low_stock_items:
                print(f" - {item.name}: Only {item.quantity} left")

    elif choice == 6:
        while True:
            reports_menu()
            choice_input_2 = input("Select an option (1–6 or 0 to top menu.): ").strip()
    
            if not choice_input_2.isdigit() or int(choice_input_2) not in range(0, 7):
                print("❌ Invalid choice. Please enter a number from 0 to 6")
                continue
            choice_2 = int(choice_input_2)

            if choice_2 == 1:
                transacts = inventory.get_transaction_history()
                print(transacts)

            elif choice_2 == 2:
                total_rev = inventory.get_inventory_value()
                print(total_rev)

            elif choice_2 == 3:
                inventory_report = inventory.get_inventory_report()
                for r in inventory_report:
                    print(r)

            elif choice_2 == 4: 
                thresh = int(input("Enter a threshold to check: "))
                results = inventory.check_low_stock(thresh)
                for r in results:
                    print(f"{r}")

            elif choice_2 == 5:
                txn_type = input("Type of transaction: ")
                results = inventory.filter_transactions_by_type(txn_type)
                for r in results:
                    print(f"{r}")

            elif choice_2 == 6:
                try:
                    start_date_str = input("Enter start date (YYYY-MM-DD): ")
                    end_date_str = input("Enter end date (YYYY-MM-DD): ")
                    
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                    results = inventory.filter_transactions_by_date(start_date, end_date)
                    for r in results:
                        print(f"{r}")
                except ValueError:
                    print("❌ Invalid date format. Please use YYYY-MM-DD.")

            elif choice_2 == 0:
                print("0 to top menu")
                break
            else:
                print("❌ Invalid choice. Please select a number from 1 to 7.")

    elif choice == 7:
        # Save inventory before exiting
        inventory.save_to_file(file_path)
        print("👋 Goodbye!")
        break
    else: 
        print("❌ Invalid choice. Please select a number from 1 to 7.")

try:
    inventory.save_to_file(file_path)
except:
    pass  # Silently fail if there's an issue saving on exit