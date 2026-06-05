import json
import os
from datetime import datetime

DATA_FILE = "data.json"

DEFAULT_DATA = {
    "1001": {
        "account_number": "1001",
        "name": "Ahmed Raza",
        "pin": "4521",
        "balance": 85000.00,
        "account_type": "Savings",
        "is_locked": False,
        "failed_attempts": 0,
        "transactions": [
            {
                "type": "credit",
                "amount": 85000.00,
                "description": "Initial deposit",
                "date": "2025-01-01 09:00:00",
                "ref": "REF000001"
            }
        ]
    },
    "1002": {
        "account_number": "1002",
        "name": "Sara Khan",
        "pin": "7890",
        "balance": 150000.00,
        "account_type": "Current",
        "is_locked": False,
        "failed_attempts": 0,
        "transactions": [
            {
                "type": "credit",
                "amount": 150000.00,
                "description": "Initial deposit",
                "date": "2025-01-01 09:00:00",
                "ref": "REF000002"
            }
        ]
    },
    "1003": {
        "account_number": "1003",
        "name": "Bilal Malik",
        "pin": "1234",
        "balance": 32500.00,
        "account_type": "Savings",
        "is_locked": False,
        "failed_attempts": 0,
        "transactions": [
            {
                "type": "credit",
                "amount": 32500.00,
                "description": "Initial deposit",
                "date": "2025-01-01 09:00:00",
                "ref": "REF000003"
            }
        ]
    }
}

def load_database():
    """Load data from JSON file. If file doesn't exist, use default data."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        save_database(DEFAULT_DATA)
        return DEFAULT_DATA
    
def save_database(database):
    """Save current database state to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(database, f, indent=4)

def get_account(database, account_number):
    """Return account dict or None if not found."""
    return database.get(account_number, None)


def account_exists(database, account_number):
    """Return True if account number exists in database."""
    return account_number in database


def generate_reference():
    """Generate a unique transaction reference number."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"REF{timestamp}"

if __name__ == "__main__":
    db = load_database()
    print("Database loaded successfully.")
    print(f"Accounts found: {list(db.keys())}")
    print(f"Ahmed's balance: PKR {db['1001']['balance']:,.2f}")
    print(f"Reference test: {generate_reference()}")