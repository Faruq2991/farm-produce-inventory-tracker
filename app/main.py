from multiprocessing import Value
from app.models.inventory import Inventory

inventory: Inventory = Inventory()


def display_menu():
    print("🌽 Farm Produce Inventory Tracker 🌽")
    print("1. Add a new produce item")
    print("2. View all produce in stock")
    print("3. Record a sale")
    print("4. View total revenue")
    print("5. Exit")

while True:
    display_menu()
    choice_input = input("Select an option (1–5): ").strip()
    if not choice_input.isdigit() or int(choice_input) not in range(1, 5):
        print("Invalid choice. Please enter a number from 1 to 5")
        continue
    choice = int(choice_input)

    if choice == 1:
        name = input("Enter Produce name: ")
        try:
            qty = int(input("Enter QTY: "))
            price = float(input("Enter Price Per Unit: "))
        except ValueError:
            print("Invalid input. Quantity must be a number and price must be a decimal.")
            continue
        inventory.add_item(name, qty, price)
        print(f"✅ '{qty}kg' of {name} added to your inventory!")

    elif choice == 2:
        inventory.list_items()

    elif choice == 3:
        name = input("Stock name: ")
        try:
            qty = int(input("Qty Sold: "))
        except ValueError:
            print("Invalid input. Quantity must be a number.")

        inventory.record_sale(name, qty)

    elif choice ==4:
        sales = inventory.get_total_revenue()
        print(f"Total Revenue: ${sales:.2f}")

    elif choice == 5:
        print("Goodbye!")
        break
    else: 
        print("Invalid choice. Please select a number from 1 to 5.")




