import sqlite3

def get_db():

    conn = sqlite3.connect("app/database/inspection_history.db")
.py
    return conn
