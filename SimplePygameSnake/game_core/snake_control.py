import random
from config.game_settings import GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.direction = 'RIGHT'
        self.body = [
            [self.x, self.y],
            [self.x - GRID_SIZE, self.y],
            [self.x - 2 * GRID_SIZE, self.y]
        ]
        self.grow_pending = False
    
    def change_direction(self, new_direction):
        opposite = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT'
        }
        if opposite.get(new_direction) != self.direction:
            self.direction = new_direction
    
    def move(self):
        if self.direction == 'UP':
            self.y -= GRID_SIZE
        elif self.direction == 'DOWN':
            self.y += GRID_SIZE
        elif self.direction == 'LEFT':
            self.x -= GRID_SIZE
        elif self.direction == 'RIGHT':
            self.x += GRID_SIZE
        
        self.body.insert(0, [self.x, self.y])
        
        if self.grow_pending:
            self.grow_pending = False
        else:
            self.body.pop()
    
    def grow(self):
        self.grow_pending = True
    
    def check_collision_with_self(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head[0] == segment[0] and head[1] == segment[1]:
                return True
        return False
    
    def check_collision_with_boundary(self):
        head = self.body[0]
        if (head[0] < 0 or head[0] >= SCREEN_WIDTH or
            head[1] < 0 or head[1] >= SCREEN_HEIGHT):
            return True
        return False
    
    def get_head_position(self):
        return self.body[0]
    
    def get_body(self):
        return self.body
    
    def set_state(self, body, direction):
        self.body = body
        self.x, self.y = body[0]
        self.direction = direction

class Food:
    def __init__(self, snake_body=None):
        self.spawn(snake_body)
    
    def spawn(self, snake_body=None):
        max_x = (SCREEN_WIDTH // GRID_SIZE) - 1
        max_y = (SCREEN_HEIGHT // GRID_SIZE) - 1
        
        while True:
            self.x = random.randint(0, max_x) * GRID_SIZE
            self.y = random.randint(0, max_y) * GRID_SIZE
            
            if snake_body is None:
                break
            
            collision = False
            for segment in snake_body:
                if segment[0] == self.x and segment[1] == self.y:
                    collision = True
                    break
            if not collision:
                break
    
    def get_position(self):
        return [self.x, self.y]
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
