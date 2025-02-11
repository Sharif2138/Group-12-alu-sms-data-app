import xml.etree.ElementTree as ET
import re
import logging
from datetime import datetime


logging.basicConfig(
    filename='unprocessed_messages.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)


def parse_date(date_str):
    """Convert date string to a standard format (YYYY-MM-DD)."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return None


def extract_amount(message):
    """Extract amount from the message and convert it to an integer."""
    match = re.search(r"(\d+)\s*RWF", message)
    return int(match.group(1)) if match else None


def extract_transaction_id(message):
    """Extract transaction ID from the message."""
    match = re.search(r"Transaction ID: (\d+)", message)
    return match.group(1) if match else None


def extract_date(message):
    """Extract and standardize the date from the message."""
    match = re.search(r"Date: (.+)$", message)
    if match:
        return parse_date(match.group(1))
    return None


def categorize_message(message):
    """
    Categorize SMS messages into predefined types and extract relevant information.
    """
    cleaned_data = {
        "category": None,
        "amount": None,
        "transaction_id": None,
        "date": None
    }

    if "You have received" in message:
        cleaned_data["category"] = "Incoming Money"
    elif "Your payment of" in message:
        cleaned_data["category"] = "Payment to Code Holder"
    elif "Transfer to Mobile Number" in message:
        cleaned_data["category"] = "Transfer to Mobile Number"
    elif "Bank Deposit" in message:
        cleaned_data["category"] = "Bank Deposit"
    elif "Airtime Bill Payment" in message:
        cleaned_data["category"] = "Airtime Bill Payment"
    elif "Cash Power Bill Payment" in message:
        cleaned_data["category"] = "Cash Power Bill Payment"
    elif "Transaction by Third Party" in message:
        cleaned_data["category"] = "Third Party Transaction"
    elif "Withdrawal from Agent" in message:
        cleaned_data["category"] = "Agent Withdrawal"
    elif "Bank Transfer" in message:
        cleaned_data["category"] = "Bank Transfer"
    elif "Internet and Voice Bundle Purchase" in message:
        cleaned_data["category"] = "Internet and Voice Bundle Purchase"


    cleaned_data["amount"] = extract_amount(message)
    cleaned_data["transaction_id"] = extract_transaction_id(message)
    cleaned_data["date"] = extract_date(message)


    if all(value is not None for value in cleaned_data.values()):
        return cleaned_data
    else:
        return None


def process_xml_file(file_path):
    """Parse the XML file, clean and categorize SMS messages, and log unprocessed ones."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    processed_data = []

    for sms in root.findall('sms'):
        body = sms.find('body').text
        
        if body:
            cleaned_data = categorize_message(body)
            if cleaned_data:
                processed_data.append(cleaned_data)
            else:
                logging.info(f"Unprocessed message: {body}")

    return processed_data


if __name__ == "__main__":
    file_path = "modified_sms.xml"
    processed_messages = process_xml_file(file_path)
    
    for message in processed_messages:
        print(message)


