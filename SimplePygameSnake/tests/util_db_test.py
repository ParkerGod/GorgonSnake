import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import sqlite3
import tempfile
import shutil
from utils import util_db


class TestUtilDB(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_db_path = util_db.DB_PATH
        util_db.DB_PATH = os.path.join(self.temp_dir, 'test.db')

    def tearDown(self):
        util_db.DB_PATH = self.original_db_path
        shutil.rmtree(self.temp_dir)

    def test_init_db(self):
        util_db.init_db()
        self.assertTrue(os.path.exists(util_db.DB_PATH))

    def test_save_and_get_high_score(self):
        util_db.init_db()
        util_db.save_game_result(100, 30)
        high_score = util_db.get_high_score()
        self.assertEqual(high_score, 100)

    def test_high_score_update(self):
        util_db.init_db()
        util_db.save_game_result(50, 20)
        util_db.save_game_result(150, 40)
        high_score = util_db.get_high_score()
        self.assertEqual(high_score, 150)

    def test_total_games(self):
        util_db.init_db()
        util_db.save_game_result(10, 5)
        util_db.save_game_result(20, 10)
        total = util_db.get_total_games()
        self.assertEqual(total, 2)

    def test_total_play_time(self):
        util_db.init_db()
        util_db.save_game_result(10, 30)
        util_db.save_game_result(20, 45)
        total_time = util_db.get_total_play_time()
        self.assertEqual(total_time, 75)

    def test_game_history(self):
        util_db.init_db()
        util_db.save_game_result(10, 5)
        util_db.save_game_result(20, 10)
        history = util_db.get_game_history(limit=5)
        self.assertEqual(len(history), 2)


if __name__ == '__main__':
    unittest.main()
