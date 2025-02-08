# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

# --- Email Account ---
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT", "your_email@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_password")  # Use an app password!
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.example.com")

# --- File Paths ---
PROCESSED_IDS_FILE = "processed_transactions.txt"  # Still here for compatibility
LOG_FILE = "error_log.txt"


# --- Service Configurations ---
SERVICE_CONFIG = {
    "credit_card_1": {
        "senders": ["alerts@card1.com"],  # Replace with your actual sender
        "subject_keywords": ["Transaction Alert"],  # Replace with actual keywords
        "parser": "parse_credit_card_1_email",
    },
    "credit_card_2": {
        "senders": ["notifications@card2.com"],  # Replace with your actual sender
        "subject_keywords": ["Purchase Notification"],  # Replace with actual keywords
        "parser": "parse_credit_card_2_email",
    },
    # Add more credit cards as needed
    "paypal": {
        "senders": ["service@paypal.com"],
        "subject_keywords": ["Payment Received", "Payment Sent", "Receipt for Your Payment"],
        "parser": "parse_paypal_email",
    },
    "venmo": {
        "senders": ["venmo@venmo.com"],
        "subject_keywords": ["paid you", "charged you"],
        "parser": "parse_venmo_email",
    },
    "bank": {
        "senders": ["alerts@mybank.com", "notifications@mybank.com"],
        "subject_keywords": ["Transaction Alert", "Debit Alert"],
        "parser": "parse_bank_email"
    }
    # Add other services as needed
}