import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.game_settings import COLOR_OPTIONS

def get_color_by_name(name):
    for color in COLOR_OPTIONS:
        if color["name"] == name:
            return color["value"]
    return None

def get_all_color_names():
    return [color["name"] for color in COLOR_OPTIONS]

def save_colors_config(background_color, snake_color, food_color):
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'game_settings.py')
    
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    bg_str = f"BACKGROUND_COLOR = {background_color}"
    snake_str = f"SNAKE_COLOR = {snake_color}"
    food_str = f"FOOD_COLOR = {food_color}"
    
    import re
    content = re.sub(r'BACKGROUND_COLOR\s*=\s*\([^)]+\)', bg_str, content)
    content = re.sub(r'SNAKE_COLOR\s*=\s*\([^)]+\)', snake_str, content)
    content = re.sub(r'FOOD_COLOR\s*=\s*\([^)]+\)', food_str, content)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(content)

def load_colors_config():
    from config.game_settings import BACKGROUND_COLOR, SNAKE_COLOR, FOOD_COLOR
    return {
        "background": BACKGROUND_COLOR,
        "snake": SNAKE_COLOR,
        "food": FOOD_COLOR
    }
