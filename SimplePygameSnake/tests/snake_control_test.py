import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_core.snake_control import SnakeControl
from config.game_settings import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, SNAKE_INITIAL_LENGTH


class TestSnakeControl(unittest.TestCase):
    def setUp(self):
        self.snake = SnakeControl()
    
    def test_initial_length(self):
        self.assertEqual(len(self.snake.get_body()), SNAKE_INITIAL_LENGTH)
    
    def test_initial_direction(self):
        self.assertEqual(self.snake.direction, KEY_RIGHT)
    
    def test_set_direction_up(self):
        self.snake.set_direction(KEY_UP)
        self.assertEqual(self.snake.next_direction, KEY_UP)
    
    def test_set_direction_down(self):
        self.snake.set_direction(KEY_DOWN)
        self.assertEqual(self.snake.next_direction, KEY_DOWN)
    
    def test_set_direction_left(self):
        self.snake.set_direction(KEY_UP)
        self.snake.move()
        self.snake.set_direction(KEY_LEFT)
        self.assertEqual(self.snake.next_direction, KEY_LEFT)
    
    def test_set_direction_right(self):
        self.snake.direction = KEY_LEFT
        self.snake.set_direction(KEY_RIGHT)
        self.assertEqual(self.snake.next_direction, KEY_RIGHT)
    
    def test_cannot_reverse_up(self):
        self.snake.set_direction(KEY_DOWN)
        self.snake.move()
        self.snake.set_direction(KEY_UP)
        self.assertEqual(self.snake.next_direction, KEY_DOWN)
    
    def test_cannot_reverse_down(self):
        self.snake.set_direction(KEY_UP)
        self.snake.move()
        self.snake.set_direction(KEY_DOWN)
        self.assertEqual(self.snake.next_direction, KEY_UP)
    
    def test_cannot_reverse_left(self):
        self.snake.set_direction(KEY_UP)
        self.snake.move()
        self.snake.set_direction(KEY_LEFT)
        self.snake.move()
        self.snake.set_direction(KEY_RIGHT)
        self.assertEqual(self.snake.next_direction, KEY_LEFT)
    
    def test_cannot_reverse_right(self):
        self.snake.move()
        self.snake.set_direction(KEY_LEFT)
        self.assertEqual(self.snake.next_direction, KEY_RIGHT)
    
    def test_move_right(self):
        initial_head = self.snake.get_head_position().copy()
        self.snake.move()
        new_head = self.snake.get_head_position()
        self.assertEqual(new_head[0], initial_head[0] + 20)
        self.assertEqual(new_head[1], initial_head[1])
    
    def test_grow(self):
        initial_length = len(self.snake.get_body())
        self.snake.grow()
        self.assertEqual(len(self.snake.get_body()), initial_length + 1)
    
    def test_get_state(self):
        state = self.snake.get_state()
        self.assertIn("body", state)
        self.assertIn("direction", state)
        self.assertIn("next_direction", state)
    
    def test_load_state(self):
        state = {
            "body": [[100, 100], [80, 100], [60, 100]],
            "direction": KEY_UP,
            "next_direction": KEY_UP
        }
        self.snake.load_state(state)
        self.assertEqual(self.snake.get_body(), [[100, 100], [80, 100], [60, 100]])
        self.assertEqual(self.snake.direction, KEY_UP)


if __name__ == '__main__':
    unittest.main()
