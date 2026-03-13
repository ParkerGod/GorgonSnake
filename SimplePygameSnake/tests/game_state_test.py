import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_core.game_state import GameState
from config.game_settings import (
    GAME_STATE_MENU,
    GAME_STATE_PLAYING,
    GAME_STATE_PAUSED,
    GAME_STATE_GAME_OVER,
    GAME_STATE_SETTINGS
)


class TestGameState(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()
    
    def test_initial_state(self):
        self.assertEqual(self.game_state.get_state(), GAME_STATE_MENU)
    
    def test_set_state_playing(self):
        self.game_state.set_state(GAME_STATE_PLAYING)
        self.assertEqual(self.game_state.get_state(), GAME_STATE_PLAYING)
    
    def test_set_state_paused(self):
        self.game_state.set_state(GAME_STATE_PAUSED)
        self.assertEqual(self.game_state.get_state(), GAME_STATE_PAUSED)
    
    def test_set_state_game_over(self):
        self.game_state.set_state(GAME_STATE_GAME_OVER)
        self.assertEqual(self.game_state.get_state(), GAME_STATE_GAME_OVER)
    
    def test_set_state_settings(self):
        self.game_state.set_state(GAME_STATE_SETTINGS)
        self.assertEqual(self.game_state.get_state(), GAME_STATE_SETTINGS)
    
    def test_is_menu(self):
        self.assertTrue(self.game_state.is_menu())
        self.game_state.set_state(GAME_STATE_PLAYING)
        self.assertFalse(self.game_state.is_menu())
    
    def test_is_playing(self):
        self.assertFalse(self.game_state.is_playing())
        self.game_state.set_state(GAME_STATE_PLAYING)
        self.assertTrue(self.game_state.is_playing())
    
    def test_is_paused(self):
        self.assertFalse(self.game_state.is_paused())
        self.game_state.set_state(GAME_STATE_PAUSED)
        self.assertTrue(self.game_state.is_paused())
    
    def test_is_game_over(self):
        self.assertFalse(self.game_state.is_game_over())
        self.game_state.set_state(GAME_STATE_GAME_OVER)
        self.assertTrue(self.game_state.is_game_over())
    
    def test_is_settings(self):
        self.assertFalse(self.game_state.is_settings())
        self.game_state.set_state(GAME_STATE_SETTINGS)
        self.assertTrue(self.game_state.is_settings())
    
    def test_score_operations(self):
        self.assertEqual(self.game_state.get_score(), 0)
        self.game_state.set_score(100)
        self.assertEqual(self.game_state.get_score(), 100)
        self.game_state.increment_score()
        self.assertEqual(self.game_state.get_score(), 110)
        self.game_state.reset_score()
        self.assertEqual(self.game_state.get_score(), 0)
    
    def test_play_time(self):
        self.assertEqual(self.game_state.get_play_time(), 0)
        self.game_state.set_play_time(60)
        self.assertEqual(self.game_state.get_play_time(), 60)
    
    def test_new_high_score(self):
        self.assertFalse(self.game_state.is_new_high())
        self.game_state.set_new_high_score(True)
        self.assertTrue(self.game_state.is_new_high())
    
    def test_get_state_data(self):
        self.game_state.set_score(50)
        self.game_state.set_play_time(30)
        data = self.game_state.get_state_data()
        self.assertEqual(data["state"], GAME_STATE_MENU)
        self.assertEqual(data["score"], 50)
        self.assertEqual(data["play_time"], 30)
    
    def test_load_state_data(self):
        data = {
            "state": GAME_STATE_PLAYING,
            "score": 100,
            "play_time": 60
        }
        self.game_state.load_state_data(data)
        self.assertEqual(self.game_state.get_state(), GAME_STATE_PLAYING)
        self.assertEqual(self.game_state.get_score(), 100)
        self.assertEqual(self.game_state.get_play_time(), 60)


if __name__ == '__main__':
    unittest.main()
