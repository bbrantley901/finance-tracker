# parsers.py
import re
import datetime
import logging

def parse_credit_card_email(body):
    """Parses credit card transaction emails."""
    try:
        date_match = re.search(r"Date:\s*(.*?)(?:\n|$)", body)
        amount_match = re.search(r"Amount:\s*\$(.*?)(?:\n|$)", body)
        merchant_match = re.search(r"Merchant:\s*(.*?)(?:\n|$)", body)

        if date_match and amount_match and merchant_match:
            date_str = date_match.group(1).strip()
            amount_str = amount_match.group(1).strip()
            merchant = merchant_match.group(1).strip()

            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                try:
                    date = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
                except ValueError:
                    try:
                        date = datetime.datetime.strptime(date_str, "%b %d, %Y").date()
                    except ValueError:
                        logging.error(f"Could not parse date: {date_str}")
                        return None
            try:
                amount = float(amount_str)
            except ValueError:
                logging.error(f"Could not parse amount: {amount_str}")
                return None

            return {
                "date": date,
                "amount": amount,
                "merchant": merchant,
                "service": "credit_card"
            }
        else:
            logging.error(f"Could not parse credit card email: Missing fields. \n {body}")
            return None

    except Exception as e:
        logging.exception(f"Error parsing credit card email: {e}\nEmail Body:\n{body}")
        return None


def parse_paypal_email(body):
    """Parses PayPal transaction emails."""
    try:
        date_match = re.search(r"Date:\s*(.*?)(?:\n|$)", body)
        amount_match = re.search(r"Amount:\s*\$(.*?)(?:\n|$)", body)
        transaction_id_match = re.search(r"Transaction ID:\s*(.*?)(?:\n|$)", body)

        if date_match and amount_match and transaction_id_match:
            date_str = date_match.group(1).strip()
            amount_str = amount_match.group(1).strip()
            transaction_id = transaction_id_match.group(1).strip()
            try:
                date = datetime.datetime.strptime(date_str, "%d %b %Y").date()
            except ValueError:
                try:
                    date = datetime.datetime.strptime(date_str, "%b %d, %Y").date()
                except ValueError:
                    logging.error(f"Could not parse date in PayPal email: {date_str}")
                    return None
            try:
                amount = float(amount_str)
            except ValueError:
                logging.error(f"Could not parse amount: {amount_str}")
                return None

            return {
                "date": date,
                "amount": amount,
                "transaction_id": transaction_id,
                "service": "paypal"
            }
        else:
            logging.error(f"Could not parse PayPal email: Missing data \nEmail Body:\n{body}")
            return None
    except Exception as e:
        logging.exception(f"Error processing paypal email: {e}\n Email Body:\n{body}")
        return None

def parse_venmo_email(body):
    """Parses Venmo transaction emails."""
    try:
        date_match = re.search(r"Date:\s*(.*?)(?:\n|$)", body)
        amount_match = re.search(r"Amount:\s*\$(.*?)(?:\n|$)", body)
        description_match = re.search(r"Note:\s*(.*?)(?:\n|$)", body)

        if date_match and amount_match and description_match:
            date_str = date_match.group(1).strip()
            amount_str = amount_match.group(1).strip()
            description = description_match.group(1).strip()

            try:
                date = datetime.datetime.strptime(date_str, "%B %d, %Y").date()
            except ValueError:
                logging.error(f"Could not parse date: {date_str}")
                return None

            try:
                amount = float(amount_str)
            except ValueError:
                logging.error(f"Could not parse amount: {amount_str}")
                return None

            return {
                "date": date,
                "amount": amount,
                "description": description,
                "service": "venmo"
            }
        else:
            logging.error(f"Could not parse Venmo email: Missing Data\n Email Body:\n{body}")
    except Exception as e:
        logging.exception(f"Error parsing venmo email: {e}\n Email Body:\n{body}")
        return None
    pass

def parse_bank_email(body):
    """Parses transaction emails from your bank."""
    try:
        date_match = re.search(r"Date:\s*(.*?)(?:\n|$)", body)
        amount_match = re.search(r"Amount:\s*(-?)\$(.*?)(?:\n|$)", body)
        description_match = re.search(r"Description:\s*(.*?)(?:\n|$)",body)

        if date_match and amount_match and description_match:
            date_str = date_match.group(1).strip()
            amount_str = amount_match.group(2).strip()
            sign = amount_match.group(1).strip()
            description = description_match.group(1).strip()

            try:
                date = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
            except ValueError:
                logging.error(f"Could not parse date: {date_str}")
                return None
            try:
                amount = float(amount_str)
                if sign == "-":
                    amount = -amount
            except ValueError:
                logging.error(f"Could not parse amount: {amount_str}")
                return None

            return {
                "date": date,
                "amount": amount,
                "description": description,
                "service": "bank"
            }
        else:
            logging.error(f"Could not parse bank email: Missing Fields\n Email Body: {body}")
            return None
    except Exception as e:
        logging.exception(f"Error parsing email from bank: {e}\n Email Body:\n{body}")
        return None
    pass