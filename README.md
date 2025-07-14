# 🌽 Farm Produce Inventory Tracker

A simple Python command-line application to manage farm produce inventory, record sales, and track total revenue. Data is persisted in a JSON file for easy backup and portability.

---

## Features

- **Add Produce:** Add new produce items with name, quantity, and price per unit.
- **View Inventory:** List all produce currently in stock.
- **Record Sales:** Record sales and automatically update inventory and revenue.
- **Revenue Tracking:** View total revenue from all sales.
- **Data Persistence:** Inventory and revenue are saved to a JSON file.

---

## Project Structure

```
farm-produce-inventory-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main CLI application
│   └── models/
│       ├── __init__.py
│       ├── inventory.py     # Inventory management logic
│       ├── produce.py       # Produce item model
│       └── transaction.py   # (Reserved for future use)
├── data/
│   └── inventory.json       # Inventory and revenue data
├── tests/
│   ├── __init__.py
│   ├── test_inventory.py    # Inventory tests
│   └── test_produce.py      # Produce item tests
├── requirements.txt         # Python dependencies (currently empty)
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd farm-produce-inventory-tracker
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(No external dependencies required by default)*

---

## Usage

### Running the Application

You must specify a data file path for inventory storage (e.g., `data/inventory.json`):

```bash
python -m app.main data/inventory.json
```

### Menu Options

1. **Add a new produce item:**  
   Enter the name, quantity (integer), and price per unit (decimal).

2. **View all produce in stock:**  
   Lists all items in inventory.

3. **Record a sale:**  
   Enter the produce name and quantity sold. Inventory and revenue are updated.

4. **View total revenue:**  
   Displays the total revenue from all sales.

5. **Exit:**  
   Saves inventory and exits the program.

---

## Data Storage

- All inventory and revenue data are stored in the JSON file you specify (e.g., `data/inventory.json`).
- The file is created automatically if it does not exist.

---

## Testing

Run the test suite with:

```bash
python -m pytest tests/
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## License

MIT License

---

## Roadmap

- [ ] Improve error handling and input validation
- [ ] Add transaction history and reporting
- [ ] Web or GUI interface
- [ ] Multi-user support
- [ ] Mobile app for field data collection
- [ ] Integration with accounting software
- [ ] Advanced reporting and analytics
- [ ] Multi-user support with role-based access
- [ ] Export to Excel/CSV formats
- [ ] Barcode scanning support
- [ ] Adding AI capabilities: 
   - Market Analysis for a particular produce.
   - Identify Comapanies that can off take from the farmer.
   - Identify local businesses or buyers.
   - Preservation techniques.

---



