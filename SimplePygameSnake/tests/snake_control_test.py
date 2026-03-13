import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from game_core.snake_control import Snake, Food
from config.game_settings import GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class TestSnakeControl(unittest.TestCase):
    def setUp(self):
        self.snake = Snake()
    
    def test_snake_initialization(self):
        self.assertEqual(len(self.snake.body), 3)
        self.assertEqual(self.snake.direction, 'RIGHT')
    
    def test_snake_movement(self):
        initial_head = self.snake.get_head_position().copy()
        self.snake.move()
        new_head = self.snake.get_head_position()
        self.assertEqual(new_head[0], initial_head[0] + GRID_SIZE)
        self.assertEqual(new_head[1], initial_head[1])
    
    def test_snake_change_direction(self):
        self.snake.change_direction('UP')
        self.assertEqual(self.snake.direction, 'UP')
    
    def test_snake_change_direction_opposite(self):
        self.snake.change_direction('LEFT')
        self.assertEqual(self.snake.direction, 'RIGHT')
    
    def test_snake_grow(self):
        initial_length = len(self.snake.body)
        self.snake.grow()
        self.snake.move()
        self.assertEqual(len(self.snake.body), initial_length + 1)
    
    def test_collision_with_boundary(self):
        self.snake.x = -GRID_SIZE
        self.snake.y = 0
        self.snake.body[0] = [-GRID_SIZE, 0]
        self.assertTrue(self.snake.check_collision_with_boundary())

class TestFood(unittest.TestCase):
    def test_food_spawn(self):
        snake = Snake()
        food = Food(snake.get_body())
        pos = food.get_position()
        self.assertGreaterEqual(pos[0], 0)
        self.assertLess(pos[0], SCREEN_WIDTH)
        self.assertGreaterEqual(pos[1], 0)
        self.assertLess(pos[1], SCREEN_HEIGHT)
    
    def test_food_position(self):
        food = Food()
        food.set_position(100, 200)
        pos = food.get_position()
        self.assertEqual(pos[0], 100)
        self.assertEqual(pos[1], 200)

if __name__ == '__main__':
    unittest.main()
