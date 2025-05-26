import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'records.db')
        self.init_db()
        self._init_window_region_table()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT NOT NULL,
                    monster TEXT NOT NULL,
                    note TEXT,
                    initial_exp TEXT,
                    final_exp TEXT,
                    total_exp TEXT,
                    exp_per_min TEXT,
                    total_time TEXT,
                    timestamp TEXT NOT NULL
                )
            ''')
    
    def _init_window_region_table(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS window_region (
                    user_id TEXT PRIMARY KEY,
                    x INTEGER,
                    y INTEGER,
                    w INTEGER,
                    h INTEGER
                )
            """)
            conn.commit()
    
    def save_record(self, user, data):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO records (
                    user, monster, note, initial_exp, final_exp, 
                    total_exp, exp_per_min, total_time, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user,
                data['怪物/副本'],
                data['備註'],
                data['初始經驗值'],
                data['最終經驗值'],
                data['總獲得經驗值'],
                data['平均每分鐘經驗值'],
                data['總計時間'],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
    
    def get_user_records(self, user):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM records WHERE user = ? ORDER BY timestamp DESC',
                (user,)
            )
            return cursor.fetchall()
    
    def delete_record(self, rec_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM records WHERE id = ?", (rec_id,))

    def get_window_region(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT x, y, w, h FROM window_region WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            if row:
                return {"x": row[0], "y": row[1], "w": row[2], "h": row[3]}
            return None

    def save_window_region(self, user_id, region):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO window_region (user_id, x, y, w, h)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    x=excluded.x, y=excluded.y, w=excluded.w, h=excluded.h
            """, (user_id, region["x"], region["y"], region["w"], region["h"]))
            conn.commit()
