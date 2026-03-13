import unittest
import os
import sys
import tempfile
import shutil
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestColorUtil(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()
        from config import game_settings
        cls.original_config_file = game_settings.CONFIG_FILE
        game_settings.CONFIG_FILE = os.path.join(cls.test_dir, "test_user_settings.json")
    
    @classmethod
    def tearDownClass(cls):
        from config import game_settings
        game_settings.CONFIG_FILE = cls.original_config_file
        shutil.rmtree(cls.test_dir)
    
    def setUp(self):
        from utils.util_color import ColorUtil
        self.color_util = ColorUtil()
    
    def test_default_colors(self):
        from config.game_settings import DEFAULT_BACKGROUND_COLOR, DEFAULT_SNAKE_COLOR, DEFAULT_FOOD_COLOR
        self.assertEqual(self.color_util.get_background_color(), DEFAULT_BACKGROUND_COLOR)
        self.assertEqual(self.color_util.get_snake_color(), DEFAULT_SNAKE_COLOR)
        self.assertEqual(self.color_util.get_food_color(), DEFAULT_FOOD_COLOR)
    
    def test_set_background_color(self):
        new_color = (100, 100, 100)
        self.color_util.set_background_color(new_color)
        self.assertEqual(self.color_util.get_background_color(), new_color)
    
    def test_set_snake_color(self):
        new_color = (0, 200, 0)
        self.color_util.set_snake_color(new_color)
        self.assertEqual(self.color_util.get_snake_color(), new_color)
    
    def test_set_food_color(self):
        new_color = (255, 100, 100)
        self.color_util.set_food_color(new_color)
        self.assertEqual(self.color_util.get_food_color(), new_color)
    
    def test_reset_to_default(self):
        self.color_util.set_background_color((50, 50, 50))
        self.color_util.set_snake_color((50, 50, 50))
        self.color_util.set_food_color((50, 50, 50))
        self.color_util.reset_to_default()
        from config.game_settings import DEFAULT_BACKGROUND_COLOR, DEFAULT_SNAKE_COLOR, DEFAULT_FOOD_COLOR
        self.assertEqual(self.color_util.get_background_color(), DEFAULT_BACKGROUND_COLOR)
        self.assertEqual(self.color_util.get_snake_color(), DEFAULT_SNAKE_COLOR)
        self.assertEqual(self.color_util.get_food_color(), DEFAULT_FOOD_COLOR)
    
    def test_get_color_list(self):
        color_list = self.color_util.get_color_list()
        self.assertIsInstance(color_list, list)
        self.assertGreater(len(color_list), 0)
        for item in color_list:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], tuple)
            self.assertEqual(len(item[1]), 3)


if __name__ == '__main__':
    unittest.main()
