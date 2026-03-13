import sqlite3
import os
from datetime import datetime

DB_PATH = './data/snake_game.db'


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL,
            duration INTEGER NOT NULL,
            play_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_stats (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            total_games INTEGER DEFAULT 0,
            total_play_time INTEGER DEFAULT 0,
            high_score INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO player_stats (id) VALUES (1)
    ''')
    conn.commit()
    conn.close()


def save_game_result(score, duration):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO game_stats (score, duration) VALUES (?, ?)',
        (score, duration)
    )
    cursor.execute(
        'UPDATE player_stats SET total_games = total_games + 1, total_play_time = total_play_time + ? WHERE id = 1',
        (duration,)
    )
    cursor.execute(
        'UPDATE player_stats SET high_score = ? WHERE id = 1 AND high_score < ?',
        (score, score)
    )
    conn.commit()
    conn.close()


def get_high_score():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT high_score FROM player_stats WHERE id = 1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def get_total_games():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT total_games FROM player_stats WHERE id = 1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def get_total_play_time():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT total_play_time FROM player_stats WHERE id = 1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def get_game_history(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT score, duration, play_date FROM game_stats ORDER BY play_date DESC LIMIT ?',
        (limit,)
    )
    results = cursor.fetchall()
    conn.close()
    return results
