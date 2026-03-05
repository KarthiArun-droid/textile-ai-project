import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "inspection_history.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
INSERT OR IGNORE INTO users (name,email,password,role)
VALUES (?,?,?,?)
""", ("Admin","admin@factory.com","admin123","admin"))

conn.commit()
conn.close()

print("Admin user created successfully")