"""
importing the flask and jsonify modules from the flask package
importing sqlite
"""
from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # enabling cross-origin access

# function for fetching data from sqlite
def get_transactions():
    conn = sqlite3.connect("mydatabase.db")  # Connect to your SQLite file
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM momo")  # Query the momo table
    rows = cursor.fetchall()  # Fetch all data
    conn.close()

    # converting to a list of dictionaries
    transactions = []
    for row in rows:
        transactions.append({
            "address": row[0],
            "date": row[1],
            "amount": row[2],
            "category": row[3],
            "transaction_id": row[4]
        })
    
    return transactions

@app.route("/transactions", methods=["GET"])
def transactions():
    return jsonify(get_transactions())  # Return data as JSON

if __name__ == "__main__":
    app.run(debug=True, port=5000)
