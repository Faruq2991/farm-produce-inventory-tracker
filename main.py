import sys
import os
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
    print("6. Exit")

while True:
    display_menu()
    choice_input = input("Select an option (1–6): ").strip()
    
    # Fixed range validation - should be 1-6, not 1-7
    if not choice_input.isdigit() or int(choice_input) not in range(1, 7):
        print("❌ Invalid choice. Please enter a number from 1 to 6")
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
        # Save inventory before exiting
        inventory.save_to_file(file_path)
        print("👋 Goodbye!")
        break
    
    else: 
        print("❌ Invalid choice. Please select a number from 1 to 6.")

try:
    inventory.save_to_file(file_path)
except:
    pass  # Silently fail if there's an issue saving on exit