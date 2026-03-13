import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.game_settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GRID_SIZE,
    FOOD_SIZE
)


class FoodControl:
    def __init__(self):
        self.position = [0, 0]
        self.size = FOOD_SIZE
        self.spawn([])
    
    def spawn(self, snake_body):
        max_x = (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE
        max_y = (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE
        while True:
            x = random.randint(0, max_x) * GRID_SIZE
            y = random.randint(0, max_y) * GRID_SIZE
            collision = False
            for segment in snake_body:
                if segment[0] == x and segment[1] == y:
                    collision = True
                    break
            if not collision:
                self.position = [x, y]
                break
    
    def get_position(self):
        return self.position
    
    def get_size(self):
        return self.size
    
    def get_state(self):
        return {
            "position": self.position.copy()
        }
    
    def load_state(self, state):
        self.position = state["position"].copy()
