"""
importing sqlite3 and csv module
"""
import sqlite3
import csv

# connecting to the database sqlite file
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

# open the csv file and read the cleaned data
with open('cleaned_data.csv') as csv_file:
    reader = csv.reader(csv_file)
    for i in reader:
        # inserting the data into the table in the database
        # i is row of the csv file
        cursor.execute("INSERT INTO momo (address, date, amount, category, transaction_id) VALUES (?, ?, ?, ?, ?)", i)
# commit changes and close the connection to the database
conn.commit()
conn.close()
