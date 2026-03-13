import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.game_settings import (
    CONFIG_FILE,
    DEFAULT_BACKGROUND_COLOR,
    DEFAULT_SNAKE_COLOR,
    DEFAULT_FOOD_COLOR
)


class ColorUtil:
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.background_color = DEFAULT_BACKGROUND_COLOR
        self.snake_color = DEFAULT_SNAKE_COLOR
        self.food_color = DEFAULT_FOOD_COLOR
        self._load_settings()
    
    def _ensure_config_dir(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
    
    def _load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.background_color = tuple(settings.get("background_color", list(DEFAULT_BACKGROUND_COLOR)))
                    self.snake_color = tuple(settings.get("snake_color", list(DEFAULT_SNAKE_COLOR)))
                    self.food_color = tuple(settings.get("food_color", list(DEFAULT_FOOD_COLOR)))
            except (json.JSONDecodeError, KeyError):
                self._save_settings()
        else:
            self._ensure_config_dir()
            self._save_settings()
    
    def _save_settings(self):
        self._ensure_config_dir()
        settings = {
            "background_color": list(self.background_color),
            "snake_color": list(self.snake_color),
            "food_color": list(self.food_color)
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    
    def set_background_color(self, color):
        self.background_color = tuple(color)
        self._save_settings()
    
    def set_snake_color(self, color):
        self.snake_color = tuple(color)
        self._save_settings()
    
    def set_food_color(self, color):
        self.food_color = tuple(color)
        self._save_settings()
    
    def get_background_color(self):
        return self.background_color
    
    def get_snake_color(self):
        return self.snake_color
    
    def get_food_color(self):
        return self.food_color
    
    def reset_to_default(self):
        self.background_color = DEFAULT_BACKGROUND_COLOR
        self.snake_color = DEFAULT_SNAKE_COLOR
        self.food_color = DEFAULT_FOOD_COLOR
        self._save_settings()
    
    @staticmethod
    def get_color_list():
        return [
            ("黑色", (0, 0, 0)),
            ("白色", (255, 255, 255)),
            ("红色", (255, 0, 0)),
            ("绿色", (0, 255, 0)),
            ("蓝色", (0, 0, 255)),
            ("黄色", (255, 255, 0)),
            ("青色", (0, 255, 255)),
            ("紫色", (255, 0, 255)),
            ("橙色", (255, 165, 0)),
            ("灰色", (128, 128, 128)),
            ("深绿", (0, 100, 0)),
            ("深蓝", (0, 0, 139)),
            ("粉红", (255, 192, 203)),
            ("棕色", (139, 69, 19)),
        ]
