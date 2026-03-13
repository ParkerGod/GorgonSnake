import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.game_settings import SAVE_FILE, SAVE_DIR


class SaveManager:
    def __init__(self):
        self.save_file = SAVE_FILE
        self._ensure_save_dir()
    
    def _ensure_save_dir(self):
        os.makedirs(SAVE_DIR, exist_ok=True)
    
    def save_game(self, snake_state, food_state, score, play_time):
        self._ensure_save_dir()
        save_data = {
            "snake": snake_state,
            "food": food_state,
            "score": score,
            "play_time": play_time
        }
        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        return True
    
    def load_game(self):
        if not os.path.exists(self.save_file):
            return None
        try:
            with open(self.save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            return save_data
        except (json.JSONDecodeError, KeyError):
            return None
    
    def has_save(self):
        return os.path.exists(self.save_file)
    
    def delete_save(self):
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
            return True
        return False
