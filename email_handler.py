# email_handler.py
import imaplib
import email
import logging
from config import EMAIL_ACCOUNT, EMAIL_PASSWORD, IMAP_SERVER, SERVICE_CONFIG, LOG_FILE

logging.basicConfig(filename=LOG_FILE, level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def get_service(msg):
    """Determines the service based on the sender and subject."""
    sender = msg["From"]
    subject = msg["Subject"]

    for service_name, config in SERVICE_CONFIG.items():
        if sender in config["senders"] and any(keyword in subject for keyword in config["subject_keywords"]):
            return service_name
    return None

def fetch_emails():
    """Connects to the IMAP server and fetches unread emails."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        if status != 'OK':
            logging.error(f"Error searching for emails: {status}")
            return []

        messages = messages[0].split()
        emails = []

        for mail_id in messages:
            status, data = mail.fetch(mail_id, "(RFC822)")
            if status != 'OK':
                logging.error(f"Error fetching email: {status}")
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            emails.append(msg)

        mail.close()
        mail.logout()
        return emails

    except Exception as e:
        logging.exception(f"Error fetching emails: {e}")
        return []