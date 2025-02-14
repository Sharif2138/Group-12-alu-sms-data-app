from flask import Flask, jsonify
from flask_cors import CORS  # To allow cross-origin requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample data (replace with data from your database)
transactions = [
    { "category": "Incoming Money", "amount": 5000, "date": "2024-01-01 10:00:00", "description": "Received 5000 RWF from John Doe" },
    { "category": "Payments to Code Holders", "amount": 1500, "date": "2024-01-02 14:30:00", "description": "Payment of 1500 RWF to Jane Smith" },
    { "category": "Transfers to Mobile Numbers", "amount": 3000, "date": "2024-01-03 16:00:00", "description": "Transferred 3000 RWF to 250123456789" },
    { "category": "Bank Deposits", "amount": 10000, "date": "2024-01-04 12:00:00", "description": "Bank deposit of 10000 RWF" },
    { "category": "Airtime Bill Payments", "amount": 2000, "date": "2024-01-05 09:00:00", "description": "Airtime purchase of 2000 RWF" },
    { "category": "Cash Power Bill Payments", "amount": 5000, "date": "2024-01-06 18:00:00", "description": "Cash Power payment of 5000 RWF" },
    { "category": "Withdrawals from Agents", "amount": 20000, "date": "2024-01-07 12:00:00", "description": "Withdrawn 20000 RWF via agent Jane Doe" },
    { "category": "Internet and Voice Bundle Purchases", "amount": 2000, "date": "2024-01-08 10:00:00", "description": "Internet bundle purchase of 2000 RWF" }
]

# API endpoint to fetch transactions
@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify(transactions)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Use port 5001
