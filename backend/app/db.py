# backend/app/db.py
import sqlite3
import time

class RequestDB:
    def __init__(self):
        self.conn = sqlite3.connect("requests.db", check_same_thread=False)
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            status TEXT,
            customer_id TEXT,
            timestamp REAL
        )
        """)
        self.conn.commit()

    def add_request(self, question, customer_id):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO requests (question, status, customer_id, timestamp) VALUES (?, ?, ?, ?)",
            (question, "pending", customer_id, time.time())
        )
        self.conn.commit()
        return c.lastrowid

    def get_pending(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM requests WHERE status='pending'")
        return c.fetchall()

    def get_request_by_id(self, request_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM requests WHERE id=?", (request_id,))
        return c.fetchone()

    def resolve_request(self, request_id):
        c = self.conn.cursor()
        c.execute("UPDATE requests SET status='resolved' WHERE id=?", (request_id,))
        self.conn.commit()
