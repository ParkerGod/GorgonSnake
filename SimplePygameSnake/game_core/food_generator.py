import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.game_settings import GRID_WIDTH, GRID_HEIGHT


class FoodGenerator:
    def __init__(self):
        self.position = None

    def generate(self, snake_body):
        all_positions = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)]
        available_positions = [pos for pos in all_positions if pos not in snake_body]
        if available_positions:
            self.position = random.choice(available_positions)
        else:
            self.position = None
        return self.position

    def get_position(self):
        return self.position

    def to_dict(self):
        return {'position': self.position}

    @classmethod
    def from_dict(cls, data):
        generator = cls.__new__(cls)
        generator.position = tuple(data['position']) if data['position'] else None
        return generator
