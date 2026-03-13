import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from game_core.food_generator import FoodGenerator


class TestFoodGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = FoodGenerator()

    def test_initial_position_none(self):
        self.assertIsNone(self.generator.get_position())

    def test_generate_food(self):
        snake_body = [(5, 5)]
        pos = self.generator.generate(snake_body)
        self.assertIsNotNone(pos)
        self.assertNotIn(pos, snake_body)

    def test_generate_avoids_snake(self):
        snake_body = [(x, y) for x in range(40) for y in range(30)]
        snake_body = snake_body[:-1]
        pos = self.generator.generate(snake_body)
        self.assertIsNotNone(pos)
        self.assertNotIn(pos, snake_body)

    def test_generate_no_space(self):
        snake_body = [(x, y) for x in range(40) for y in range(30)]
        pos = self.generator.generate(snake_body)
        self.assertIsNone(pos)

    def test_to_dict(self):
        self.generator.position = (10, 10)
        data = self.generator.to_dict()
        self.assertEqual(data['position'], (10, 10))

    def test_from_dict(self):
        data = {'position': [15, 20]}
        generator = FoodGenerator.from_dict(data)
        self.assertEqual(generator.get_position(), (15, 20))


if __name__ == '__main__':
    unittest.main()
