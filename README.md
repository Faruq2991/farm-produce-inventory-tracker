# 🌽 Farm Produce Inventory Tracker

A Python application to manage farm produce inventory, record sales, and track total revenue. Features both a command-line interface (CLI) and a RESTful API backend (FastAPI). Data is persisted in a JSON file for easy backup and portability.

---

## Features

- **Add Produce:** Add new produce items with name, quantity, price per unit, category, and unit.
- **View Inventory:** List all produce currently in stock.
- **Record Sales:** Record sales and automatically update inventory and revenue.
- **Revenue Tracking:** View total revenue from all sales.
- **Reporting:** Generate inventory and transaction reports.
- **Data Persistence:** Inventory and revenue are saved to a JSON file.
- **REST API:** (Coming soon) Manage inventory via HTTP endpoints.
- **Web Frontend:** (Planned) User-friendly web interface for inventory management.

---

## Project Structure

```
farm-produce-inventory-tracker/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── inventory.py      # Inventory management logic
│   │   ├── produce.py        # Produce item model
│   │   └── transaction.py    # Transaction model
│   ├── api/                  # FastAPI routes (to be created)
│   │   ├── __init__.py
│   │   └── endpoints.py      # API endpoints (to be created)
│   └── main.py               # FastAPI app entrypoint (to be created)
├── frontend/                 # Web frontend (to be created)
│   └── ...
├── data/
│   └── inventory.json        # Inventory and revenue data
├── tests/
│   ├── __init__.py
│   ├── test_inventory.py     # Inventory tests
│   └── test_produce.py       # Produce item tests
├── main.py                   # CLI application entrypoint
├── requirements.txt          # Python dependencies
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

---

## Usage

### Running the CLI Application

You must specify a data file path for inventory storage (e.g., `data/inventory.json`):

```bash
python main.py data/inventory.json
```

### Running the FastAPI Backend (Coming Soon)

The backend API will be available via FastAPI. To run the API server:

```bash
uvicorn app.main:app --reload
```

API docs will be available at `http://localhost:8000/docs`.

### Running the Web Frontend (Planned)

The frontend will be located in the `frontend/` directory. Instructions will be provided once implemented.

---

## Data Storage

- All inventory and revenue data are stored in the JSON file you specify (e.g., `data/inventory.json`).
- The file is created automatically if it does not exist.

---

## Testing

Run the test suite with:

```bash
python -m unittest discover tests/
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

- [x] CLI: Inventory management, sales, and reporting
- [ ] FastAPI backend (in progress)
- [ ] Web frontend (planned)
- [ ] Improve error handling and input validation
- [ ] Multi-user support
- [ ] Mobile app for field data collection
- [ ] Integration with accounting software
- [ ] Advanced reporting and analytics
- [ ] Export to Excel/CSV formats
- [ ] Barcode scanning support
- [ ] AI capabilities (market analysis, buyer identification, preservation techniques)
- [ ] CLI enhancements (search/filter, low-stock warnings)
- [ ] Advanced tests (parametrized, CLI automation)

---



