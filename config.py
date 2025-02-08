# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

# --- Email Account ---
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT", "your_email@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_password")  # Use an app password!
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.example.com")

# --- File Paths ---
PROCESSED_IDS_FILE = "processed_transactions.txt"  # No longer strictly needed, but kept for compatibility.
LOG_FILE = "error_log.txt"


# --- Service Configurations ---
SERVICE_CONFIG = {
    "credit_card": {
        "senders": ["alerts@mycreditcard.com", "notifications@mycreditcard.com"],
        "subject_keywords": ["Transaction Alert", "Purchase Notification"],
        "parser": "parse_credit_card_email",
    },
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
}