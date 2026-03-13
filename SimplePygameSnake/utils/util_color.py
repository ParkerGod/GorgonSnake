import json
import os

COLOR_CONFIG_PATH = './data/color_config.json'

DEFAULT_COLORS = {
    'bg_color': [0, 0, 0],
    'snake_color': [0, 255, 0],
    'food_color': [255, 0, 0]
}


def load_colors():
    if os.path.exists(COLOR_CONFIG_PATH):
        try:
            with open(COLOR_CONFIG_PATH, 'r', encoding='utf-8') as f:
                colors = json.load(f)
                return (
                    tuple(colors.get('bg_color', DEFAULT_COLORS['bg_color'])),
                    tuple(colors.get('snake_color', DEFAULT_COLORS['snake_color'])),
                    tuple(colors.get('food_color', DEFAULT_COLORS['food_color']))
                )
        except (json.JSONDecodeError, KeyError):
            pass
    return (
        tuple(DEFAULT_COLORS['bg_color']),
        tuple(DEFAULT_COLORS['snake_color']),
        tuple(DEFAULT_COLORS['food_color'])
    )


def save_colors(bg_color, snake_color, food_color):
    os.makedirs(os.path.dirname(COLOR_CONFIG_PATH), exist_ok=True)
    colors = {
        'bg_color': list(bg_color),
        'snake_color': list(snake_color),
        'food_color': list(food_color)
    }
    with open(COLOR_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(colors, f, indent=4)


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)
