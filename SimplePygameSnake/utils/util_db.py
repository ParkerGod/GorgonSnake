import sqlite3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.game_settings import DB_PATH


class DatabaseUtil:
    def __init__(self):
        self.db_path = DB_PATH
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT DEFAULT 'Player',
                high_score INTEGER DEFAULT 0,
                total_play_time INTEGER DEFAULT 0,
                total_games INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS score_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                play_time INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute("SELECT COUNT(*) FROM game_stats")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO game_stats (player_name, high_score, total_play_time, total_games)
                VALUES ('Player', 0, 0, 0)
            ''')
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_game_stats(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT high_score, total_play_time, total_games FROM game_stats WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        if result:
            return {
                "high_score": result[0],
                "total_play_time": result[1],
                "total_games": result[2]
            }
        return {"high_score": 0, "total_play_time": 0, "total_games": 0}
    
    def update_high_score(self, score):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE game_stats SET high_score = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1", (score,))
        conn.commit()
        conn.close()
    
    def increment_play_time(self, seconds):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE game_stats SET total_play_time = total_play_time + ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1", (seconds,))
        conn.commit()
        conn.close()
    
    def increment_total_games(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE game_stats SET total_games = total_games + 1, updated_at = CURRENT_TIMESTAMP WHERE id = 1")
        conn.commit()
        conn.close()
    
    def save_score_history(self, score, play_time):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO score_history (score, play_time) VALUES (?, ?)
        ''', (score, play_time))
        conn.commit()
        conn.close()
    
    def get_score_history(self, limit=10):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT score, play_time, created_at FROM score_history ORDER BY created_at DESC LIMIT ?", (limit,))
        results = cursor.fetchall()
        conn.close()
        return [{"score": r[0], "play_time": r[1], "created_at": r[2]} for r in results]
    
    def update_game_end(self, score, play_time):
        self.increment_total_games()
        self.increment_play_time(play_time)
        self.save_score_history(score, play_time)
        stats = self.get_game_stats()
        if score > stats["high_score"]:
            self.update_high_score(score)
        return score > stats["high_score"]
