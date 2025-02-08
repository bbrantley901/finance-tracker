# data_handler.py
import hashlib
import os
import csv
import logging
import datetime
from config import PROCESSED_IDS_FILE, LOG_FILE

TRANSACTIONS_CSV = "transactions.csv"

def load_processed_ids():
    """Loads previously processed transaction IDs from the CSV file."""
    processed_ids = set()
    if os.path.exists(TRANSACTIONS_CSV):
        with open(TRANSACTIONS_CSV, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                processed_ids.add(row['transaction_id'])
    return processed_ids

def generate_transaction_id(transaction_data):
    """Creates a unique ID for a transaction."""
    if transaction_data.get("service") == "paypal" and transaction_data.get("transaction_id"):
        return "paypal_" + transaction_data["transaction_id"]

    data_string = f"{transaction_data.get('service', 'unknown')}-{transaction_data['date']}-{transaction_data['amount']}-{transaction_data.get('merchant', transaction_data.get('description', ''))}"
    return hashlib.sha256(data_string.encode()).hexdigest()

def load_transactions():
    """Loads all transactions from the CSV file."""
    transactions = []
    if os.path.exists(TRANSACTIONS_CSV):
        with open(TRANSACTIONS_CSV, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['date'] = datetime.datetime.strptime(row['date'], '%Y-%m-%d').date()
                row['amount'] = float(row['amount'])
                transactions.append(row)
    return transactions

def calculate_net_cost(transactions):
    """Calculates the net cost from a list of transactions."""
    net_cost = 0
    for transaction in transactions:
        net_cost += transaction['amount']
    return net_cost

def process_transaction(transaction_data, processed_ids):
    """Processes a transaction, saves to CSV, and updates net cost."""
    transaction_id = generate_transaction_id(transaction_data)

    if transaction_id not in processed_ids:
        transaction_data['transaction_id'] = transaction_id

        fieldnames = ['transaction_id', 'date', 'amount', 'merchant', 'description', 'service']
        for field in fieldnames:
            if field not in transaction_data:
                transaction_data[field] = ''

        write_header = not os.path.exists(TRANSACTIONS_CSV)
        with open(TRANSACTIONS_CSV, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow(transaction_data)

        print(f"New Transaction: {transaction_data}")
        return True
    else:
        print(f"Duplicate transaction skipped: {transaction_data}")
        return False