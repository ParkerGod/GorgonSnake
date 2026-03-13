import json
import os
import time
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_core.snake_control import Snake
from game_core.food_generator import FoodGenerator
from utils.util_db import save_game_result, get_high_score, init_db
from config.game_settings import SAVE_PATH, DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT


class GameLogic:
    def __init__(self):
        init_db()
        self.snake = None
        self.food_generator = None
        self.score = 0
        self.game_over = False
        self.paused = False
        self.start_time = None
        self.duration = 0
        self.high_score = get_high_score()

    def new_game(self):
        self.snake = Snake()
        self.food_generator = FoodGenerator()
        self.food_generator.generate(self.snake.get_body())
        self.score = 0
        self.game_over = False
        self.paused = False
        self.start_time = time.time()
        self.duration = 0
        self.high_score = get_high_score()

    def update(self):
        if self.game_over or self.paused:
            return
        
        self.snake.move()
        
        if self.snake.check_wall_collision() or self.snake.check_self_collision():
            self.game_over = True
            self.duration = int(time.time() - self.start_time)
            save_game_result(self.score, self.duration)
            self.high_score = get_high_score()
            return
        
        if self.snake.get_head() == self.food_generator.get_position():
            self.snake.grow()
            self.score += 10
            self.food_generator.generate(self.snake.get_body())

    def handle_input(self, key):
        if self.game_over:
            return
        
        if key == 'UP':
            self.snake.set_direction(DIRECTION_UP)
        elif key == 'DOWN':
            self.snake.set_direction(DIRECTION_DOWN)
        elif key == 'LEFT':
            self.snake.set_direction(DIRECTION_LEFT)
        elif key == 'RIGHT':
            self.snake.set_direction(DIRECTION_RIGHT)

    def toggle_pause(self):
        self.paused = not self.paused

    def save_game(self):
        if self.snake is None or self.game_over:
            return False
        
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
        save_data = {
            'snake': self.snake.to_dict(),
            'food': self.food_generator.to_dict(),
            'score': self.score,
            'duration': int(time.time() - self.start_time)
        }
        with open(SAVE_PATH, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=4)
        return True

    def load_game(self):
        if not os.path.exists(SAVE_PATH):
            return False
        
        try:
            with open(SAVE_PATH, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            self.snake = Snake.from_dict(save_data['snake'])
            self.food_generator = FoodGenerator.from_dict(save_data['food'])
            self.score = save_data['score']
            self.game_over = False
            self.paused = False
            self.start_time = time.time() - save_data.get('duration', 0)
            self.duration = save_data.get('duration', 0)
            self.high_score = get_high_score()
            return True
        except (json.JSONDecodeError, KeyError, TypeError):
            return False

    def get_snake_body(self):
        return self.snake.get_body() if self.snake else []

    def get_food_position(self):
        return self.food_generator.get_position() if self.food_generator else None

    def get_score(self):
        return self.score

    def is_game_over(self):
        return self.game_over

    def is_paused(self):
        return self.paused

    def get_high_score(self):
        return self.high_score
