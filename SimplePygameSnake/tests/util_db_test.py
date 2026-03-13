import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile
import sqlite3
from utils.util_db import init_database, get_game_stats, save_game_result

class TestUtilDB(unittest.TestCase):
    def setUp(self):
        import config.game_settings as settings
        self.original_path = settings.DATABASE_PATH
        settings.DATABASE_PATH = ":memory:"
        
        from utils import util_db
        util_db.DATABASE_PATH = ":memory:"
    
    def test_init_database(self):
        init_database()
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
    
    def test_get_game_stats(self):
        stats = get_game_stats()
        self.assertEqual(len(stats), 3)
        self.assertIsInstance(stats[0], int)
        self.assertIsInstance(stats[1], int)
        self.assertIsInstance(stats[2], (int, float))

if __name__ == '__main__':
    unittest.main()
