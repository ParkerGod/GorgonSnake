import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import patch, MagicMock
from game_core.game_logic import GameLogic


class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.game = GameLogic()

    @patch('game_core.game_logic.save_game_result')
    @patch('game_core.game_logic.get_high_score')
    def test_new_game(self, mock_high_score, mock_save):
        mock_high_score.return_value = 100
        self.game.new_game()
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.paused)
        self.assertIsNotNone(self.game.snake)
        self.assertIsNotNone(self.game.food_generator)

    def test_handle_input(self):
        self.game.new_game()
        self.game.handle_input('UP')
        self.game.update()
        head = self.game.get_snake_body()[0]
        self.assertEqual(head[1], 14)

    def test_game_over_on_wall_collision(self):
        self.game.new_game()
        self.game.snake.body = [(0, 0)]
        self.game.snake.direction = (-1, 0)
        self.game.snake.next_direction = (-1, 0)
        self.game.update()
        self.assertTrue(self.game.is_game_over())

    def test_score_increase_on_eat(self):
        self.game.new_game()
        self.game.snake.body = [(5, 5)]
        self.game.food_generator.position = (6, 5)
        self.game.snake.direction = (1, 0)
        self.game.snake.next_direction = (1, 0)
        initial_score = self.game.score
        self.game.update()
        if self.game.snake.get_head() == self.game.food_generator.get_position():
            self.assertEqual(self.game.score, initial_score + 10)

    def test_toggle_pause(self):
        self.game.new_game()
        self.assertFalse(self.game.is_paused())
        self.game.toggle_pause()
        self.assertTrue(self.game.is_paused())
        self.game.toggle_pause()
        self.assertFalse(self.game.is_paused())

    def test_get_score(self):
        self.game.new_game()
        self.assertEqual(self.game.get_score(), 0)
        self.game.score = 50
        self.assertEqual(self.game.get_score(), 50)


if __name__ == '__main__':
    unittest.main()
