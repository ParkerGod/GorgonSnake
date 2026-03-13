import pygame
import sys
import time
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.game_settings import (
    GAME_FPS,
    SNAKE_SPEED,
    GAME_STATE_MENU,
    GAME_STATE_PLAYING,
    GAME_STATE_PAUSED,
    GAME_STATE_GAME_OVER,
    GAME_STATE_SETTINGS,
    KEY_UP,
    KEY_DOWN,
    KEY_LEFT,
    KEY_RIGHT
)
from game_core import SnakeControl, FoodControl, GameRender, SaveManager, GameState
from utils import DatabaseUtil, ColorUtil


class SnakeGame:
    def __init__(self):
        self.renderer = GameRender()
        self.snake = SnakeControl()
        self.food = FoodControl()
        self.game_state = GameState()
        self.save_manager = SaveManager()
        self.db_util = DatabaseUtil()
        self.color_util = ColorUtil()
        
        self.clock = self.renderer.get_clock()
        self.running = True
        self.last_move_time = 0
        self.move_interval = 1000 // SNAKE_SPEED
        self.game_start_time = 0
        self.settings_selected = 0
        self.message_display_time = 0
        self.message_type = None
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state.is_settings():
                    self.handle_settings_click(event.pos)
    
    def handle_keydown(self, key):
        if self.game_state.is_menu():
            self.handle_menu_key(key)
        elif self.game_state.is_playing():
            self.handle_playing_key(key)
        elif self.game_state.is_paused():
            self.handle_paused_key(key)
        elif self.game_state.is_game_over():
            self.handle_game_over_key(key)
        elif self.game_state.is_settings():
            self.handle_settings_key(key)
    
    def handle_menu_key(self, key):
        if key == pygame.K_SPACE:
            self.start_new_game()
        elif key == pygame.K_s:
            self.load_saved_game()
        elif key == pygame.K_c:
            self.game_state.set_state(GAME_STATE_SETTINGS)
            self.settings_selected = 0
        elif key == pygame.K_ESCAPE:
            self.running = False
    
    def handle_playing_key(self, key):
        if key == pygame.K_UP:
            self.snake.set_direction(KEY_UP)
        elif key == pygame.K_DOWN:
            self.snake.set_direction(KEY_DOWN)
        elif key == pygame.K_LEFT:
            self.snake.set_direction(KEY_LEFT)
        elif key == pygame.K_RIGHT:
            self.snake.set_direction(KEY_RIGHT)
        elif key == pygame.K_p:
            self.game_state.set_state(GAME_STATE_PAUSED)
        elif key == pygame.K_ESCAPE:
            self.game_state.set_state(GAME_STATE_MENU)
    
    def handle_paused_key(self, key):
        if key == pygame.K_p:
            self.game_state.set_state(GAME_STATE_PLAYING)
        elif key == pygame.K_s:
            self.save_game()
        elif key == pygame.K_ESCAPE:
            self.game_state.set_state(GAME_STATE_MENU)
    
    def handle_game_over_key(self, key):
        if key == pygame.K_r:
            self.start_new_game()
        elif key == pygame.K_ESCAPE:
            self.game_state.set_state(GAME_STATE_MENU)
    
    def handle_settings_key(self, key):
        if key == pygame.K_UP:
            self.settings_selected = (self.settings_selected - 1) % 3
        elif key == pygame.K_DOWN:
            self.settings_selected = (self.settings_selected + 1) % 3
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.cycle_color(self.settings_selected, key == pygame.K_RIGHT)
        elif key == pygame.K_ESCAPE:
            self.game_state.set_state(GAME_STATE_MENU)
    
    def handle_settings_click(self, pos):
        color_list = self.color_util.get_color_list()
        start_x = 450
        for i, (_, color) in enumerate(color_list):
            x = start_x + (i % 7) * 50
            y = 120 + (i // 7) * 50
            if x <= pos[0] <= x + 40 and y <= pos[1] <= y + 40:
                self.set_color_by_index(self.settings_selected, color)
                break
    
    def cycle_color(self, setting_index, forward):
        color_list = self.color_util.get_color_list()
        current_colors = [
            self.color_util.get_background_color(),
            self.color_util.get_snake_color(),
            self.color_util.get_food_color()
        ]
        current_color = current_colors[setting_index]
        current_idx = 0
        for i, (_, color) in enumerate(color_list):
            if color == current_color:
                current_idx = i
                break
        if forward:
            new_idx = (current_idx + 1) % len(color_list)
        else:
            new_idx = (current_idx - 1) % len(color_list)
        new_color = color_list[new_idx][1]
        self.set_color_by_index(setting_index, new_color)
    
    def set_color_by_index(self, index, color):
        if index == 0:
            self.color_util.set_background_color(color)
        elif index == 1:
            self.color_util.set_snake_color(color)
        elif index == 2:
            self.color_util.set_food_color(color)
    
    def start_new_game(self):
        self.snake.reset()
        self.food.spawn(self.snake.get_body())
        self.game_state.reset_score()
        self.game_state.set_state(GAME_STATE_PLAYING)
        self.game_start_time = time.time()
        self.last_move_time = pygame.time.get_ticks()
    
    def load_saved_game(self):
        save_data = self.save_manager.load_game()
        if save_data:
            self.snake.load_state(save_data["snake"])
            self.food.load_state(save_data["food"])
            self.game_state.set_score(save_data["score"])
            self.game_state.set_play_time(save_data["play_time"])
            self.game_state.set_state(GAME_STATE_PLAYING)
            self.game_start_time = time.time() - save_data["play_time"]
            self.last_move_time = pygame.time.get_ticks()
        else:
            self.message_type = "load_failed"
            self.message_display_time = pygame.time.get_ticks()
            self.start_new_game()
    
    def save_game(self):
        snake_state = self.snake.get_state()
        food_state = self.food.get_state()
        current_play_time = int(time.time() - self.game_start_time)
        self.save_manager.save_game(snake_state, food_state, self.game_state.get_score(), current_play_time)
        self.message_type = "save_success"
        self.message_display_time = pygame.time.get_ticks()
    
    def update(self):
        if self.game_state.is_playing():
            current_time = pygame.time.get_ticks()
            if current_time - self.last_move_time >= self.move_interval:
                self.last_move_time = current_time
                self.snake.move()
                if self.snake.check_collision_with_point(self.food.get_position()):
                    self.snake.grow()
                    self.game_state.increment_score()
                    self.food.spawn(self.snake.get_body())
                if self.snake.check_collision_with_walls() or self.snake.check_collision_with_self():
                    self.end_game()
        
        if self.message_type and pygame.time.get_ticks() - self.message_display_time > 1500:
            self.message_type = None
    
    def end_game(self):
        play_time = int(time.time() - self.game_start_time)
        is_new_high = self.db_util.update_game_end(self.game_state.get_score(), play_time)
        self.game_state.set_new_high_score(is_new_high)
        self.game_state.set_state(GAME_STATE_GAME_OVER)
    
    def render(self):
        if self.game_state.is_menu():
            stats = self.db_util.get_game_stats()
            self.renderer.draw_menu(stats["high_score"], stats["total_games"], stats["total_play_time"])
        elif self.game_state.is_playing():
            self.renderer.clear_screen(self.color_util.get_background_color())
            self.renderer.draw_food(self.food.get_position(), self.color_util.get_food_color())
            self.renderer.draw_snake(self.snake.get_body(), self.color_util.get_snake_color())
            self.renderer.draw_score(self.game_state.get_score())
        elif self.game_state.is_paused():
            self.renderer.clear_screen(self.color_util.get_background_color())
            self.renderer.draw_food(self.food.get_position(), self.color_util.get_food_color())
            self.renderer.draw_snake(self.snake.get_body(), self.color_util.get_snake_color())
            self.renderer.draw_score(self.game_state.get_score())
            self.renderer.draw_pause()
            if self.message_type == "save_success":
                self.renderer.draw_save_success()
        elif self.game_state.is_game_over():
            self.renderer.clear_screen(self.color_util.get_background_color())
            self.renderer.draw_food(self.food.get_position(), self.color_util.get_food_color())
            self.renderer.draw_snake(self.snake.get_body(), self.color_util.get_snake_color())
            stats = self.db_util.get_game_stats()
            self.renderer.draw_game_over(
                self.game_state.get_score(),
                stats["high_score"],
                self.game_state.is_new_high()
            )
        elif self.game_state.is_settings():
            self.renderer.draw_settings(self.color_util, self.settings_selected)
        
        self.renderer.update()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(GAME_FPS)
        
        pygame.quit()
        sys.exit()


def main():
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()
