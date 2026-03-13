import unittest
import os
import sys
import tempfile
import shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSaveManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()
        from config import game_settings
        cls.original_save_dir = game_settings.SAVE_DIR
        cls.original_save_file = game_settings.SAVE_FILE
        game_settings.SAVE_DIR = cls.test_dir
        game_settings.SAVE_FILE = os.path.join(cls.test_dir, "savedata_1.json")
    
    @classmethod
    def tearDownClass(cls):
        from config import game_settings
        game_settings.SAVE_DIR = cls.original_save_dir
        game_settings.SAVE_FILE = cls.original_save_file
        shutil.rmtree(cls.test_dir)
    
    def setUp(self):
        from game_core.save_manager import SaveManager
        self.save_manager = SaveManager()
    
    def test_save_game(self):
        snake_state = {
            "body": [[100, 100], [80, 100], [60, 100]],
            "direction": "RIGHT",
            "next_direction": "RIGHT"
        }
        food_state = {"position": [200, 200]}
        result = self.save_manager.save_game(snake_state, food_state, 50, 30)
        self.assertTrue(result)
    
    def test_load_game(self):
        snake_state = {
            "body": [[100, 100], [80, 100], [60, 100]],
            "direction": "RIGHT",
            "next_direction": "RIGHT"
        }
        food_state = {"position": [200, 200]}
        self.save_manager.save_game(snake_state, food_state, 50, 30)
        
        loaded_data = self.save_manager.load_game()
        self.assertIsNotNone(loaded_data)
        self.assertEqual(loaded_data["score"], 50)
        self.assertEqual(loaded_data["play_time"], 30)
        self.assertEqual(loaded_data["snake"]["body"], [[100, 100], [80, 100], [60, 100]])
    
    def test_load_game_no_file(self):
        if os.path.exists(self.save_manager.save_file):
            os.remove(self.save_manager.save_file)
        result = self.save_manager.load_game()
        self.assertIsNone(result)
    
    def test_has_save(self):
        if os.path.exists(self.save_manager.save_file):
            os.remove(self.save_manager.save_file)
        self.assertFalse(self.save_manager.has_save())
        
        snake_state = {"body": [[100, 100]], "direction": "RIGHT", "next_direction": "RIGHT"}
        food_state = {"position": [200, 200]}
        self.save_manager.save_game(snake_state, food_state, 10, 5)
        self.assertTrue(self.save_manager.has_save())
    
    def test_delete_save(self):
        snake_state = {"body": [[100, 100]], "direction": "RIGHT", "next_direction": "RIGHT"}
        food_state = {"position": [200, 200]}
        self.save_manager.save_game(snake_state, food_state, 10, 5)
        self.assertTrue(self.save_manager.has_save())
        
        self.save_manager.delete_save()
        self.assertFalse(self.save_manager.has_save())


if __name__ == '__main__':
    unittest.main()
