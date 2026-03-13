import sqlite3
import os
import time

from config.game_settings import DATABASE_PATH

def init_database():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            play_count INTEGER DEFAULT 0,
            highest_score INTEGER DEFAULT 0,
            total_play_time REAL DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER,
            play_time REAL,
            play_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM game_stats')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO game_stats (play_count, highest_score, total_play_time) VALUES (0, 0, 0)')
    
    conn.commit()
    conn.close()

def get_game_stats():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT play_count, highest_score, total_play_time FROM game_stats WHERE id = 1')
    result = cursor.fetchone()
    conn.close()
    return result if result else (0, 0, 0)

def save_game_result(score, play_time):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO game_history (score, play_time) VALUES (?, ?)', (score, play_time))
    
    cursor.execute('SELECT play_count, highest_score, total_play_time FROM game_stats WHERE id = 1')
    stats = cursor.fetchone()
    
    new_play_count = stats[0] + 1
    new_highest_score = max(stats[1], score)
    new_total_time = stats[2] + play_time
    
    cursor.execute('''
        UPDATE game_stats 
        SET play_count = ?, highest_score = ?, total_play_time = ? 
        WHERE id = 1
    ''', (new_play_count, new_highest_score, new_total_time))
    
    conn.commit()
    conn.close()
