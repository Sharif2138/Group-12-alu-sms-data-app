import xml.etree.ElementTree as ET
import re
import csv
from datetime import datetime

def clean_and_categorize_sms(xml_file: str) -> list:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    categorized_sms = []

    for sms in root.findall('sms'):
        body = sms.attrib.get('body', "")
        date = sms.attrib.get('date', None)
        address = sms.attrib.get('address', "Unknown")
        transaction_id = extract_transaction_id(body)

        
        amount = extract_amount(body)
        if date:
            date = datetime.fromtimestamp(int(date) / 1000).strftime('%Y-%m-%d %H:%M:%S')

        category = categorize_sms(body.lower())

        if amount is not None and date: 
            categorized_sms.append({
                "address": address,
                "date": date,
                "amount": amount,
                "category": category,
                "transaction_id": transaction_id
            })

    return categorized_sms

def extract_transaction_id(body: str) -> str:
    """Extracts the transaction ID from the SMS body."""
    match = re.search(r'TxId:\s*(\d+)', body)  
    if match:
        return match.group(1)
    match = re.search(r'\bTransaction Id:\s*(\d+)', body) 
    if match:
        return match.group(1)
    return "N/A"

def extract_amount(body: str) -> int:
    """Extracts the first amount in RWF from the SMS body."""
    match = re.search(r'\b(\d{1,7})\s*RWF\b', body)
    if match:
        return int(match.group(1))
    return None

def categorize_sms(body: str) -> str:
    """Categorizes the SMS based on keywords found in the body."""
    if "you have received" in body and "from" in body:
        return "Incoming Money"
    elif "your payment of" in body and "has been completed" in body:
        return "Payments to Code Holders"
    elif "bank deposit" in body:
        return "Bank Deposits"
    elif "transferred to" in body and "(" in body and ")" in body:
        return "Transfers to Mobile Numbers"
    elif "airtime" in body:
        return "Airtime Bill Payments"
    elif "a transaction of" in body and "by" in body:
        return "Transactions Initiated by Third Parties"
    elif "withdrawn" in body:
        return "Withdrawals from Agents"
    return "Uncategorized"

def write_to_csv(sms_data: list, output_file: str):
    """Writes the cleaned and categorized SMS data to a CSV file."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["address", "date", "amount", "category", "transaction_id"])
        writer.writeheader()
        writer.writerows(sms_data)

if __name__ == "__main__":
    sms_data = clean_and_categorize_sms('modified_sms_v2.xml')
    write_to_csv(sms_data, 'cleaned_data.csv')
    print("Data has been successfully written to cleaned_data.csv.")
