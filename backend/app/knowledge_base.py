# backend/app/knowledge_base.py

import sqlite3

class KnowledgeBase:
    def __init__(self):
        # persistent SQLite DB
        self.conn = sqlite3.connect("kb.db", check_same_thread=False)
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            question TEXT PRIMARY KEY,
            answer TEXT
        )
        """)
        self.conn.commit()  # <- must commit table creation

    def get_answer(self, question):
        c = self.conn.cursor()
        c.execute("SELECT answer FROM answers WHERE question=?", (question,))
        row = c.fetchone()
        return row[0] if row else None

    def learn_answer(self, question, answer):
        c = self.conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO answers (question, answer) VALUES (?, ?)",
            (question, answer)
        )
        self.conn.commit()  # <- must commit insert
        print(f"KnowledgeBase: Learned answer for '{question}'")
