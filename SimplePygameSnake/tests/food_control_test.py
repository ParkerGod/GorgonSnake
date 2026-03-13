import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_core.food_control import FoodControl
from config.game_settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE


class TestFoodControl(unittest.TestCase):
    def setUp(self):
        self.food = FoodControl()
    
    def test_spawn_position_valid(self):
        pos = self.food.get_position()
        self.assertGreaterEqual(pos[0], 0)
        self.assertGreaterEqual(pos[1], 0)
        self.assertLess(pos[0], SCREEN_WIDTH)
        self.assertLess(pos[1], SCREEN_HEIGHT)
    
    def test_spawn_position_aligned(self):
        pos = self.food.get_position()
        self.assertEqual(pos[0] % GRID_SIZE, 0)
        self.assertEqual(pos[1] % GRID_SIZE, 0)
    
    def test_spawn_avoids_snake(self):
        snake_body = [[100, 100], [80, 100], [60, 100]]
        self.food.spawn(snake_body)
        pos = self.food.get_position()
        for segment in snake_body:
            self.assertNotEqual(pos, segment)
    
    def test_get_state(self):
        state = self.food.get_state()
        self.assertIn("position", state)
    
    def test_load_state(self):
        state = {"position": [200, 200]}
        self.food.load_state(state)
        self.assertEqual(self.food.get_position(), [200, 200])


if __name__ == '__main__':
    unittest.main()
