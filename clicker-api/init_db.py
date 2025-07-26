import sqlite3
import os

os.makedirs('db', exist_ok=True)
conn = sqlite3.connect('db/database.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price INTEGER NOT NULL,
    account TEXT NOT NULL
)
""")

conn.commit()
conn.close()
print("Veritabanı oluşturuldu.")
