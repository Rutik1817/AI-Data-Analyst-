import sqlite3

conn = sqlite3.connect("amazon.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

cursor.execute("SELECT * FROM customers;")
print(cursor.fetchall())

conn.close()