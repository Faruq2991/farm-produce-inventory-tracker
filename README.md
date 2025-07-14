# Farm Produce Inventory Tracker

A Python-based command-line application for managing farm produce inventory, tracking transactions, and maintaining detailed records of agricultural products.

## Description

The Farm Produce Inventory Tracker is a comprehensive CLI tool designed to help farmers and agricultural businesses manage their produce inventory efficiently. The application provides functionality to:

- **Track Produce Items**: Manage different types of farm produce with details like name, category, and unit of measurement
- **Inventory Management**: Monitor current stock levels, track additions and removals
- **Transaction History**: Record and view all inventory transactions including sales, purchases, and adjustments
- **Data Persistence**: Store all data in JSON format for easy backup and portability
- **Reporting**: Generate reports on inventory status and transaction history

### Project Structure

```
farm-produce-inventory-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main CLI application entry point
│   └── models/
│       ├── __init__.py
│       ├── inventory.py     # Inventory management logic
│       ├── produce.py       # Produce item definitions
│       └── transaction.py   # Transaction tracking
├── data/
│   └── inventory.json       # Data storage file
├── tests/
│   ├── __init__.py
│   └── test_inventory.py   # Unit tests
├── requirements.txt         # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## How to Set Up the Project Locally

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd farm-produce-inventory-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Verify installation**
   ```bash
   python -c "import sys; print(f'Python {sys.version}')"
   ```

### Development Setup

For development, you may want to install additional tools:

```bash
pip install pytest  # For running tests
pip install black   # For code formatting
pip install flake8  # For linting
```

## How to Run the CLI

### Basic Usage

Once the project is set up, you can run the CLI application using:

```bash
python -m app.main
```

### Available Commands

The CLI provides the following main commands:

#### Inventory Management
```bash
# Add new produce item
python -m app.main add-produce --name "Tomatoes" --category "Vegetables" --unit "kg"

# View current inventory
python -m app.main list-inventory

# Update stock levels
python -m app.main update-stock --item "Tomatoes" --quantity 50 --type "add"
python -m app.main update-stock --item "Tomatoes" --quantity 10 --type "remove"
```

#### Transaction Tracking
```bash
# Record a sale
python -m app.main record-sale --item "Tomatoes" --quantity 5 --price 2.50

# Record a purchase
python -m app.main record-purchase --item "Seeds" --quantity 100 --price 0.10

# View transaction history
python -m app.main list-transactions
```

#### Reporting
```bash
# Generate inventory report
python -m app.main report --type inventory

# Generate sales report
python -m app.main report --type sales

# Export data
python -m app.main export --format json
```

### Command Examples

```bash
# Initialize the application (first time setup)
python -m app.main init

# Add multiple produce items
python -m app.main add-produce --name "Apples" --category "Fruits" --unit "kg"
python -m app.main add-produce --name "Carrots" --category "Vegetables" --unit "kg"
python -m app.main add-produce --name "Eggs" --category "Dairy" --unit "dozen"

# Check current inventory
python -m app.main list-inventory

# Record some transactions
python -m app.main record-sale --item "Apples" --quantity 10 --price 3.00
python -m app.main record-purchase --item "Carrots" --quantity 25 --price 1.50

# Generate a comprehensive report
python -m app.main report --type all
```

### Data Storage

All data is stored in the `data/inventory.json` file. This file contains:
- Produce item definitions
- Current inventory levels
- Transaction history

**Note**: The data file is automatically created when you first run the application. Make sure to backup this file regularly.

## Testing

Run the test suite to ensure everything is working correctly:

```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions about the Farm Produce Inventory Tracker, please:

1. Check the existing issues in the repository
2. Create a new issue with detailed information about your problem
3. Include your operating system and Python version in the issue description

## Roadmap

- [ ] Web interface for easier data entry
- [ ] Mobile app for field data collection
- [ ] Integration with accounting software
- [ ] Advanced reporting and analytics
- [ ] Multi-user support with role-based access
- [ ] Export to Excel/CSV formats
- [ ] Barcode scanning support
