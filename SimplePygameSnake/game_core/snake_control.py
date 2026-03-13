import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.game_settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SNAKE_SIZE,
    SNAKE_INITIAL_LENGTH,
    GRID_SIZE,
    KEY_UP,
    KEY_DOWN,
    KEY_LEFT,
    KEY_RIGHT
)


class SnakeControl:
    def __init__(self):
        self.snake_body = []
        self.direction = KEY_RIGHT
        self.next_direction = KEY_RIGHT
        self.size = SNAKE_SIZE
        self.initial_length = SNAKE_INITIAL_LENGTH
        self.reset()
    
    def reset(self):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        self.snake_body = []
        for i in range(self.initial_length):
            self.snake_body.append([center_x - i * GRID_SIZE, center_y])
        self.direction = KEY_RIGHT
        self.next_direction = KEY_RIGHT
    
    def set_direction(self, new_direction):
        if new_direction == KEY_UP and self.direction != KEY_DOWN:
            self.next_direction = KEY_UP
        elif new_direction == KEY_DOWN and self.direction != KEY_UP:
            self.next_direction = KEY_DOWN
        elif new_direction == KEY_LEFT and self.direction != KEY_RIGHT:
            self.next_direction = KEY_LEFT
        elif new_direction == KEY_RIGHT and self.direction != KEY_LEFT:
            self.next_direction = KEY_RIGHT
    
    def move(self):
        self.direction = self.next_direction
        head = self.snake_body[0].copy()
        if self.direction == KEY_UP:
            head[1] -= GRID_SIZE
        elif self.direction == KEY_DOWN:
            head[1] += GRID_SIZE
        elif self.direction == KEY_LEFT:
            head[0] -= GRID_SIZE
        elif self.direction == KEY_RIGHT:
            head[0] += GRID_SIZE
        self.snake_body.insert(0, head)
        self.snake_body.pop()
    
    def grow(self):
        tail = self.snake_body[-1].copy()
        self.snake_body.append(tail)
    
    def get_head_position(self):
        return self.snake_body[0]
    
    def get_body(self):
        return self.snake_body
    
    def get_length(self):
        return len(self.snake_body)
    
    def check_collision_with_walls(self):
        head = self.snake_body[0]
        if head[0] < 0 or head[0] >= SCREEN_WIDTH:
            return True
        if head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True
        return False
    
    def check_collision_with_self(self):
        head = self.snake_body[0]
        for segment in self.snake_body[1:]:
            if head[0] == segment[0] and head[1] == segment[1]:
                return True
        return False
    
    def check_collision_with_point(self, point):
        head = self.snake_body[0]
        return head[0] == point[0] and head[1] == point[1]
    
    def get_state(self):
        return {
            "body": [segment.copy() for segment in self.snake_body],
            "direction": self.direction,
            "next_direction": self.next_direction
        }
    
    def load_state(self, state):
        self.snake_body = [segment.copy() for segment in state["body"]]
        self.direction = state["direction"]
        self.next_direction = state["next_direction"]
