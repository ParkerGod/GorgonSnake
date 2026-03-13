import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_core.game_logic import GameLogic
from game_core.game_render import GameRenderer
from utils.util_db import init_db, get_high_score, get_total_games
from utils.util_color import load_colors, save_colors
from config.game_settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SNAKE_SPEED,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT
)


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = 'MENU'
        self.game_logic = GameLogic()
        
        bg_color, snake_color, food_color = load_colors()
        self.renderer = GameRenderer(self.screen, bg_color, snake_color, food_color)
        self.colors = {
            'bg': list(bg_color),
            'snake': list(snake_color),
            'food': list(food_color)
        }
        self.selected_color_option = 0
        self.color_adjust_index = 0
        
        init_db()

    def run(self):
        while self.running:
            if self.game_state == 'MENU':
                self.handle_menu()
            elif self.game_state == 'PLAYING':
                self.handle_playing()
            elif self.game_state == 'PAUSED':
                self.handle_paused()
            elif self.game_state == 'GAME_OVER':
                self.handle_game_over()
            elif self.game_state == 'COLOR_SETTINGS':
                self.handle_color_settings()
            
            self.clock.tick(SNAKE_SPEED)

        pygame.quit()
        sys.exit()

    def handle_menu(self):
        high_score = get_high_score()
        total_games = get_total_games()
        self.renderer.draw_main_menu(high_score, total_games)
        self.renderer.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_logic.new_game()
                    self.game_state = 'PLAYING'
                elif event.key == pygame.K_l:
                    if self.game_logic.load_game():
                        self.game_state = 'PLAYING'
                elif event.key == pygame.K_c:
                    self.game_state = 'COLOR_SETTINGS'
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def handle_playing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game_logic.handle_input('UP')
                elif event.key == pygame.K_DOWN:
                    self.game_logic.handle_input('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.game_logic.handle_input('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.game_logic.handle_input('RIGHT')
                elif event.key == pygame.K_p:
                    self.game_logic.toggle_pause()
                    self.game_state = 'PAUSED'
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = 'MENU'

        self.game_logic.update()
        
        if self.game_logic.is_game_over():
            self.game_state = 'GAME_OVER'
            return

        self.renderer.clear()
        self.renderer.draw_snake(self.game_logic.get_snake_body())
        food_pos = self.game_logic.get_food_position()
        if food_pos:
            self.renderer.draw_food(food_pos)
        self.renderer.draw_score(self.game_logic.get_score(), self.game_logic.get_high_score())
        self.renderer.update()

    def handle_paused(self):
        self.renderer.draw_pause_menu()
        self.renderer.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game_logic.toggle_pause()
                    self.game_state = 'PLAYING'
                elif event.key == pygame.K_s:
                    self.game_logic.save_game()
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = 'MENU'

    def handle_game_over(self):
        self.renderer.draw_game_over(self.game_logic.get_score())
        self.renderer.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game_logic.new_game()
                    self.game_state = 'PLAYING'
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = 'MENU'

    def handle_color_settings(self):
        bg = tuple(self.colors['bg'])
        snake = tuple(self.colors['snake'])
        food = tuple(self.colors['food'])
        
        self.renderer.draw_color_settings(bg, snake, food, self.selected_color_option)
        self.renderer.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = 'MENU'
                elif event.key == pygame.K_UP:
                    self.selected_color_option = (self.selected_color_option - 1) % 3
                    self.color_adjust_index = 0
                elif event.key == pygame.K_DOWN:
                    self.selected_color_option = (self.selected_color_option + 1) % 3
                    self.color_adjust_index = 0
                elif event.key == pygame.K_LEFT:
                    self.color_adjust_index = (self.color_adjust_index - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    self.color_adjust_index = (self.color_adjust_index + 1) % 3
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    color_key = ['bg', 'snake', 'food'][self.selected_color_option]
                    self.colors[color_key][self.color_adjust_index] = min(
                        255, self.colors[color_key][self.color_adjust_index] + 15
                    )
                    self.update_renderer_colors()
                elif event.key == pygame.K_MINUS:
                    color_key = ['bg', 'snake', 'food'][self.selected_color_option]
                    self.colors[color_key][self.color_adjust_index] = max(
                        0, self.colors[color_key][self.color_adjust_index] - 15
                    )
                    self.update_renderer_colors()
                elif event.key == pygame.K_RETURN:
                    save_colors(
                        tuple(self.colors['bg']),
                        tuple(self.colors['snake']),
                        tuple(self.colors['food'])
                    )
                    self.game_state = 'MENU'

    def update_renderer_colors(self):
        self.renderer.set_colors(
            tuple(self.colors['bg']),
            tuple(self.colors['snake']),
            tuple(self.colors['food'])
        )


if __name__ == '__main__':
    game = SnakeGame()
    game.run()
