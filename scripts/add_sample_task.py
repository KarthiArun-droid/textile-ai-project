import sqlite3
from datetime import date

conn = sqlite3.connect("inspection_history.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO production_tasks (order_id, process, status, planned_date)
VALUES (?, ?, ?, ?)
""", ("ORD101", "Dyeing", "Pending", date.today()))

conn.commit()
conn.close()

print("Sample task added")