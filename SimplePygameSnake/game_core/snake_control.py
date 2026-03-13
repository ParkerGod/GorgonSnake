import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.game_settings import (
    GRID_WIDTH, GRID_HEIGHT,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT
)


class Snake:
    def __init__(self, start_pos=None):
        if start_pos is None:
            start_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.body = [start_pos]
        self.direction = DIRECTION_RIGHT
        self.next_direction = DIRECTION_RIGHT
        self.grow_pending = 0

    def set_direction(self, direction):
        opposite = (-self.direction[0], -self.direction[1])
        if direction != opposite:
            self.next_direction = direction

    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        new_head = (
            head_x + self.direction[0],
            head_y + self.direction[1]
        )
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
        return new_head

    def grow(self, amount=1):
        self.grow_pending += amount

    def check_self_collision(self):
        return self.body[0] in self.body[1:]

    def check_wall_collision(self):
        head_x, head_y = self.body[0]
        return head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT

    def get_head(self):
        return self.body[0]

    def get_body(self):
        return self.body.copy()

    def to_dict(self):
        return {
            'body': self.body,
            'direction': self.direction,
            'next_direction': self.next_direction,
            'grow_pending': self.grow_pending
        }

    @classmethod
    def from_dict(cls, data):
        snake = cls.__new__(cls)
        snake.body = [tuple(pos) for pos in data['body']]
        snake.direction = tuple(data['direction'])
        snake.next_direction = tuple(data['next_direction'])
        snake.grow_pending = data['grow_pending']
        return snake
