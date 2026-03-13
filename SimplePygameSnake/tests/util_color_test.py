import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile
import shutil
import json
from utils import util_color


class TestUtilColor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_config_path = util_color.COLOR_CONFIG_PATH
        util_color.COLOR_CONFIG_PATH = os.path.join(self.temp_dir, 'color_config.json')

    def tearDown(self):
        util_color.COLOR_CONFIG_PATH = self.original_config_path
        shutil.rmtree(self.temp_dir)

    def test_load_default_colors(self):
        bg, snake, food = util_color.load_colors()
        self.assertEqual(bg, (0, 0, 0))
        self.assertEqual(snake, (0, 255, 0))
        self.assertEqual(food, (255, 0, 0))

    def test_save_and_load_colors(self):
        util_color.save_colors((10, 20, 30), (40, 50, 60), (70, 80, 90))
        bg, snake, food = util_color.load_colors()
        self.assertEqual(bg, (10, 20, 30))
        self.assertEqual(snake, (40, 50, 60))
        self.assertEqual(food, (70, 80, 90))

    def test_hex_to_rgb(self):
        self.assertEqual(util_color.hex_to_rgb('#FF0000'), (255, 0, 0))
        self.assertEqual(util_color.hex_to_rgb('#00FF00'), (0, 255, 0))
        self.assertEqual(util_color.hex_to_rgb('#0000FF'), (0, 0, 255))

    def test_rgb_to_hex(self):
        self.assertEqual(util_color.rgb_to_hex((255, 0, 0)), '#ff0000')
        self.assertEqual(util_color.rgb_to_hex((0, 255, 0)), '#00ff00')
        self.assertEqual(util_color.rgb_to_hex((0, 0, 255)), '#0000ff')

    def test_load_corrupted_file(self):
        with open(util_color.COLOR_CONFIG_PATH, 'w') as f:
            f.write('invalid json')
        bg, snake, food = util_color.load_colors()
        self.assertEqual(bg, (0, 0, 0))
        self.assertEqual(snake, (0, 255, 0))
        self.assertEqual(food, (255, 0, 0))


if __name__ == '__main__':
    unittest.main()
