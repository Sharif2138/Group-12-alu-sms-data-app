import xml.etree.ElementTree as ET
import re
import logging
from datetime import datetime
import pandas as pd


logging.basicConfig(
    filename='unprocessed_messages.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def parse_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return None

def extract_amount(message):
    match = re.search(r"([\d,]+)\s*RWF", message)
    if match:
        amount = match.group(1).replace(",", "")
        logging.info(f"Extracted Amount: {amount}")
        return int(amount)
    return None

def extract_transaction_id(message):
    match = re.search(r"(?:Transaction|Ref(?:erence)?)\s*ID[:\s]+([\w\d-]+)", message, re.IGNORECASE)

    if match:
        logging.info(f"Extracted Transaction ID: {match.group(1)}")
        return match.group(1)
    return None

def extract_date(message):
    match = re.search(r"Date[:\s]+([\d-]+ [\d:]+)", message)
    if match:
        extracted_date = match.group(1)
        print(f"Extracted Date: {extracted_date}")
        return parse_date(extracted_date)
    return None

def categorize_message(message):
    cleaned_data = {
        "category": "Other",
        "amount": extract_amount(message),
        "transaction_id": extract_transaction_id(message),
        "date": extract_date(message)
    }

    msg_lower = message.lower()

    if "you have received" in msg_lower:
        cleaned_data["category"] = "Incoming Money"
    elif "your payment of" in msg_lower or "payment to code holder" in msg_lower:
        cleaned_data["category"] = "Payments to Code Holders"
    elif "transfer to mobile number" in msg_lower or "sent to" in msg_lower:
        cleaned_data["category"] = "Transfers to Mobile Numbers"
    elif "bank deposit" in msg_lower:
        cleaned_data["category"] = "Bank Deposits"
    elif "airtime bill payment" in msg_lower or "airtime purchase" in msg_lower:
        cleaned_data["category"] = "Airtime Bill Payments"
    elif "cash power bill payment" in msg_lower:
        cleaned_data["category"] = "Cash Power Bill Payments"
    elif "transaction by third party" in msg_lower or "third party transaction" in msg_lower:
        cleaned_data["category"] = "Transactions Initiated by Third Parties"
    elif "withdrawal from agent" in msg_lower or "agent withdrawal" in msg_lower:
        cleaned_data["category"] = "Withdrawals from Agents"
    elif "bank transfer" in msg_lower:
        cleaned_data["category"] = "Bank Transfers"
    elif "internet bundle" in msg_lower or "voice bundle" in msg_lower:
        cleaned_data["category"] = "Internet and Voice Bundle Purchases"

    return cleaned_data

def process_xml_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError:
        logging.error(f"Error parsing XML file: {file_path}")
        return []

    processed_data = []

    for sms in root.findall('sms'):
        body = sms.get('body')  # FIXED: Get the 'body' attribute correctly
        if body:
            cleaned_data = categorize_message(body)
            if cleaned_data:
                processed_data.append(cleaned_data)
            else:
                logging.info(f"Unprocessed message: {body}")
        else:
            logging.info("Skipped an SMS with missing <body> tag.")

    return processed_data

if __name__ == "__main__":
    file_path = "modified_sms_v2.xml"
    processed_messages = process_xml_file(file_path)

    df = pd.DataFrame(processed_messages)
    df.to_csv("cleaned_sms_data.csv", index=False)

    print("Data cleaned and saved as cleaned_sms_data.csv")
