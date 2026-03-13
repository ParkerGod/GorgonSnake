import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from game_core.snake_control import Snake
from config.game_settings import (
    GRID_WIDTH, GRID_HEIGHT,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT
)


class TestSnake(unittest.TestCase):
    def setUp(self):
        self.snake = Snake((5, 5))

    def test_initial_position(self):
        self.assertEqual(self.snake.get_head(), (5, 5))
        self.assertEqual(len(self.snake.get_body()), 1)

    def test_initial_direction(self):
        self.assertEqual(self.snake.direction, DIRECTION_RIGHT)

    def test_move_right(self):
        self.snake.move()
        self.assertEqual(self.snake.get_head(), (6, 5))

    def test_move_up(self):
        self.snake.set_direction(DIRECTION_UP)
        self.snake.move()
        self.assertEqual(self.snake.get_head(), (5, 4))

    def test_move_down(self):
        self.snake.set_direction(DIRECTION_DOWN)
        self.snake.move()
        self.assertEqual(self.snake.get_head(), (5, 6))

    def test_move_left(self):
        self.snake.set_direction(DIRECTION_UP)
        self.snake.move()
        self.snake.set_direction(DIRECTION_LEFT)
        self.snake.move()
        self.assertEqual(self.snake.get_head(), (4, 4))

    def test_reverse_direction_blocked(self):
        self.snake.set_direction(DIRECTION_LEFT)
        self.snake.move()
        self.assertEqual(self.snake.get_head(), (6, 5))

    def test_grow(self):
        self.snake.grow()
        self.snake.move()
        self.assertEqual(len(self.snake.get_body()), 2)

    def test_self_collision_false(self):
        self.assertFalse(self.snake.check_self_collision())

    def test_self_collision_true(self):
        self.snake.body = [(5, 5), (6, 5), (5, 5)]
        self.assertTrue(self.snake.check_self_collision())

    def test_wall_collision_left(self):
        self.snake.body = [(0, 5)]
        self.snake.direction = DIRECTION_LEFT
        self.snake.next_direction = DIRECTION_LEFT
        self.snake.move()
        self.assertTrue(self.snake.check_wall_collision())

    def test_wall_collision_right(self):
        self.snake.body = [(GRID_WIDTH - 1, 5)]
        self.snake.set_direction(DIRECTION_RIGHT)
        self.snake.move()
        self.assertTrue(self.snake.check_wall_collision())

    def test_wall_collision_top(self):
        self.snake.body = [(5, 0)]
        self.snake.set_direction(DIRECTION_UP)
        self.snake.move()
        self.assertTrue(self.snake.check_wall_collision())

    def test_wall_collision_bottom(self):
        self.snake.body = [(5, GRID_HEIGHT - 1)]
        self.snake.set_direction(DIRECTION_DOWN)
        self.snake.move()
        self.assertTrue(self.snake.check_wall_collision())

    def test_to_dict(self):
        self.snake.grow()
        data = self.snake.to_dict()
        self.assertEqual(data['body'], [(5, 5)])
        self.assertEqual(data['direction'], DIRECTION_RIGHT)
        self.assertEqual(data['grow_pending'], 1)

    def test_from_dict(self):
        data = {
            'body': [[5, 5], [4, 5]],
            'direction': [0, 1],
            'next_direction': [0, 1],
            'grow_pending': 0
        }
        snake = Snake.from_dict(data)
        self.assertEqual(snake.get_body(), [(5, 5), (4, 5)])
        self.assertEqual(snake.direction, (0, 1))


if __name__ == '__main__':
    unittest.main()
