from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Dict



class Transaction:
    """Enhanced transaction class with better validation and features."""
    
    VALID_TYPES = {"sale", "purchase", "adjustment", "refund"}
    
    def __init__(self, type: str, produce_name: str, quantity: float, 
                 unit_price: float, note: str = "", timestamp: Optional[str] = None):
        """
        Initialize a transaction.
        
        Args:
            type: Transaction type (sale, purchase, adjustment, refund)
            produce_name: Name of the produce item
            quantity: Quantity involved in transaction
            unit_price: Price per unit
            note: Additional notes
            timestamp: Transaction timestamp (auto-generated if None)
        """
        if type.lower() not in self.VALID_TYPES:
            raise ValueError(f"Invalid transaction type '{type}'. Must be one of: {', '.join(self.VALID_TYPES)}")
        
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if unit_price < 0:
            raise ValueError("Unit price cannot be negative")
        
        self.type = type.lower()
        self.produce_name = produce_name.strip()
        self.quantity = quantity
        self.unit_price = unit_price
        self.note = note.strip()
        self.timestamp = timestamp or datetime.now().isoformat()

    @property
    def total_amount(self) -> Decimal:
        """Calculate total transaction amount."""
        return Decimal(str(self.quantity)) * Decimal(str(self.unit_price))

    def __str__(self) -> str:
        """String representation of transaction."""
        timestamp_dt = datetime.fromisoformat(self.timestamp)
        formatted_time = timestamp_dt.strftime("%Y-%m-%d %H:%M")
        
        return (f"[{formatted_time}] {self.type.upper()}: {self.quantity} {self.produce_name} "
                f"@ ${self.unit_price:.2f} each (Total: ${self.total_amount:.2f})"
                f"{' - ' + self.note if self.note else ''}")

    def to_dict(self) -> Dict:
        """Convert transaction to dictionary for JSON serialization."""
        return {
            "type": self.type,
            "produce_name": self.produce_name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "note": self.note,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Transaction':
        """Create Transaction from dictionary."""
        return cls(
            type=data["type"],
            produce_name=data["produce_name"],
            quantity=data["quantity"],
            unit_price=data["unit_price"],
            note=data.get("note", ""),
            timestamp=data.get("timestamp")
        )