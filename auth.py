import getpass
import time
from database import load_database, save_database, get_account, account_exists

MAX_ATTEMPTS = 3
LOCKOUT_MESSAGE = "Your account has been locked due to too many failed attempts. Please visit your branch."


def get_account_number(database):
    """Ask user for account number and validate it exists."""
    while True:
        account_number = input("\n  Enter account number: ").strip()

        if not account_number:
            print("  Account number cannot be empty.")
            continue

        if not account_exists(database, account_number):
            print(f"  Account {account_number} not found. Please try again.")
            continue

        return account_number


def is_account_locked(database, account_number):
    """Check if account is locked before allowing login attempt."""
    account = get_account(database, account_number)
    return account["is_locked"]


def validate_pin(database, account_number):
    """Validate PIN with max 3 attempts. Returns True if correct, False if locked."""
    account = get_account(database, account_number)
    attempts = account["failed_attempts"]

    while attempts < MAX_ATTEMPTS:
        pin = getpass.getpass("  Enter PIN: ")

        if pin == account["pin"]:
            account["failed_attempts"] = 0
            save_database(database)
            return True

        attempts += 1
        account["failed_attempts"] = attempts
        remaining = MAX_ATTEMPTS - attempts

        if remaining > 0:
            print(f"  Wrong PIN. {remaining} attempt(s) remaining.")
            time.sleep(1)

    account["is_locked"] = True
    save_database(database)
    print(f"\n  {LOCKOUT_MESSAGE}")
    return False


def create_session(database, account_number):
    """Create a session object for the logged-in user."""
    account = get_account(database, account_number)
    return {
        "account_number": account_number,
        "name": account["name"],
        "account_type": account["account_type"],
        "is_logged_in": True
    }


def login(database):
    """Main login flow. Returns session dict if successful, None if failed."""
    print("\n  Please log in to continue.")

    account_number = get_account_number(database)

    if is_account_locked(database, account_number):
        print(f"\n  {LOCKOUT_MESSAGE}")
        return None

    pin_valid = validate_pin(database, account_number)

    if not pin_valid:
        return None

    session = create_session(database, account_number)
    print(f"\n  Welcome back, {session['name']}!")
    time.sleep(1)
    return session