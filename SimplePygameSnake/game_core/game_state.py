import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.game_settings import (
    GAME_STATE_MENU,
    GAME_STATE_PLAYING,
    GAME_STATE_PAUSED,
    GAME_STATE_GAME_OVER,
    GAME_STATE_SETTINGS
)


class GameState:
    def __init__(self):
        self.current_state = GAME_STATE_MENU
        self.score = 0
        self.play_time = 0
        self.start_time = 0
        self.is_new_high_score = False
    
    def set_state(self, state):
        self.current_state = state
    
    def get_state(self):
        return self.current_state
    
    def is_menu(self):
        return self.current_state == GAME_STATE_MENU
    
    def is_playing(self):
        return self.current_state == GAME_STATE_PLAYING
    
    def is_paused(self):
        return self.current_state == GAME_STATE_PAUSED
    
    def is_game_over(self):
        return self.current_state == GAME_STATE_GAME_OVER
    
    def is_settings(self):
        return self.current_state == GAME_STATE_SETTINGS
    
    def set_score(self, score):
        self.score = score
    
    def get_score(self):
        return self.score
    
    def increment_score(self):
        self.score += 10
    
    def reset_score(self):
        self.score = 0
    
    def set_play_time(self, time):
        self.play_time = time
    
    def get_play_time(self):
        return self.play_time
    
    def set_new_high_score(self, is_new):
        self.is_new_high_score = is_new
    
    def is_new_high(self):
        return self.is_new_high_score
    
    def get_state_data(self):
        return {
            "state": self.current_state,
            "score": self.score,
            "play_time": self.play_time
        }
    
    def load_state_data(self, data):
        self.current_state = data.get("state", GAME_STATE_MENU)
        self.score = data.get("score", 0)
        self.play_time = data.get("play_time", 0)
