import sqlite3

conn = sqlite3.connect("inspection_history.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'inspector'
    )
    """)

    # INSPECTIONS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inspections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        image TEXT,
        defect_count INTEGER,
        status TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()

init_db()