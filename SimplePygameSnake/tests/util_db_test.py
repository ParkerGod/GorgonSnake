import unittest
import os
import sys
import tempfile
import shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDatabaseUtil(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()
        cls.original_db_path = None
        from config import game_settings
        cls.original_db_path = game_settings.DB_PATH
        game_settings.DB_PATH = os.path.join(cls.test_dir, "test_snake_game.db")
    
    @classmethod
    def tearDownClass(cls):
        from config import game_settings
        game_settings.DB_PATH = cls.original_db_path
        shutil.rmtree(cls.test_dir)
    
    def setUp(self):
        from utils.util_db import DatabaseUtil
        self.db_util = DatabaseUtil()
    
    def test_get_game_stats_initial(self):
        stats = self.db_util.get_game_stats()
        self.assertEqual(stats["high_score"], 0)
        self.assertEqual(stats["total_play_time"], 0)
        self.assertEqual(stats["total_games"], 0)
    
    def test_update_high_score(self):
        self.db_util.update_high_score(100)
        stats = self.db_util.get_game_stats()
        self.assertEqual(stats["high_score"], 100)
    
    def test_increment_play_time(self):
        initial_stats = self.db_util.get_game_stats()
        initial_time = initial_stats["total_play_time"]
        self.db_util.increment_play_time(30)
        stats = self.db_util.get_game_stats()
        self.assertEqual(stats["total_play_time"], initial_time + 30)
    
    def test_increment_total_games(self):
        initial_stats = self.db_util.get_game_stats()
        initial_games = initial_stats["total_games"]
        self.db_util.increment_total_games()
        stats = self.db_util.get_game_stats()
        self.assertEqual(stats["total_games"], initial_games + 1)
    
    def test_save_score_history(self):
        self.db_util.save_score_history(50, 60)
        history = self.db_util.get_score_history(1)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["score"], 50)
        self.assertEqual(history[0]["play_time"], 60)


if __name__ == '__main__':
    unittest.main()
