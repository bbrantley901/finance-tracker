# main.py
import email_handler
import data_handler
import parsers
from config import SERVICE_CONFIG, LOG_FILE
import logging
import datetime

logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

def main():
    processed_ids = data_handler.load_processed_ids()
    emails = email_handler.fetch_emails()
    transactions = data_handler.load_transactions()
    net_cost = data_handler.calculate_net_cost(transactions)
    print(f"Current Net Cost: ${net_cost:.2f}")

    for msg in emails:
        service = email_handler.get_service(msg)

        if service:
            parser_name = SERVICE_CONFIG[service]["parser"]
            parser_function = getattr(parsers, parser_name)

            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
            else:
                logging.error(f"No text/plain part found in email from {msg['From']} - {msg['Subject']}")
                continue

            transaction_data = parser_function(body)

            if transaction_data:
                if data_handler.process_transaction(transaction_data, processed_ids):
                    net_cost += transaction_data['amount']
            else:
                logging.warning(f"Failed to parse email from {msg['From']} - {msg['Subject']}")
        else:
           logging.warning(f"Unknown sender or subject: {msg['From']} - {msg['Subject']}")

    print(f"Updated Net Cost: ${net_cost:.2f}")

if __name__ == "__main__":
    main()