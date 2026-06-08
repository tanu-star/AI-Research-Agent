import sqlite3
from typing import Optional, List
import json
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Database:
    def __init__(self, db_name: str = "research.db"):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS research_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query TEXT NOT NULL,
                results TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_user(self, username: str, email: str, password: str) -> bool:
        conn = self.get_connection()
        c = conn.cursor()
        hashed = pwd_context.hash(password)
        try:
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                     (username, email, hashed))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()
    
    def get_user_by_username(self, username: str) -> Optional[dict]:
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "username": row[1], "email": row[2], "password": row[3]}
        return None
    
    def verify_user(self, username: str, password: str) -> Optional[dict]:
        user = self.get_user_by_username(username)
        if user and pwd_context.verify(password, user["password"]):
            return {"id": user["id"], "username": user["username"]}
        return None
    
    def save_research(self, user_id: int, query: str, results: List[dict]) -> bool:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO research_history (user_id, query, results) VALUES (?, ?, ?)",
                     (user_id, query, json.dumps(results)))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()
    
    def get_history(self, user_id: int, limit: int = 10) -> List[dict]:
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM research_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
                 (user_id, limit))
        rows = c.fetchall()
        conn.close()
        return [
            {"id": r[0], "query": r[2], "results": r[3], "created_at": r[4]}
            for r in rows
        ]

db = Database()
