import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.game_settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE,
    FONT_SIZE, TITLE_FONT_SIZE
)


class GameRenderer:
    def __init__(self, screen, bg_color=(0, 0, 0), snake_color=(0, 255, 0), food_color=(255, 0, 0)):
        self.screen = screen
        self.bg_color = bg_color
        self.snake_color = snake_color
        self.food_color = food_color
        pygame.font.init()
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.title_font = pygame.font.SysFont(None, TITLE_FONT_SIZE)

    def set_colors(self, bg_color=None, snake_color=None, food_color=None):
        if bg_color:
            self.bg_color = bg_color
        if snake_color:
            self.snake_color = snake_color
        if food_color:
            self.food_color = food_color

    def clear(self):
        self.screen.fill(self.bg_color)

    def draw_snake(self, snake_body):
        for i, segment in enumerate(snake_body):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            if i == 0:
                color = (
                    max(0, self.snake_color[0] - 30),
                    max(0, self.snake_color[1] - 30),
                    max(0, self.snake_color[2] - 30)
                )
            else:
                color = self.snake_color
            pygame.draw.rect(self.screen, color, (x, y, GRID_SIZE - 1, GRID_SIZE - 1))

    def draw_food(self, food_pos):
        x = food_pos[0] * GRID_SIZE
        y = food_pos[1] * GRID_SIZE
        pygame.draw.rect(self.screen, self.food_color, (x, y, GRID_SIZE - 1, GRID_SIZE - 1))

    def draw_score(self, score, high_score=0):
        score_text = self.font.render(f'Score: {score}', True, (255, 255, 255))
        high_score_text = self.font.render(f'High Score: {high_score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))

    def draw_game_over(self, score):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.title_font.render('GAME OVER', True, (255, 0, 0))
        score_text = self.font.render(f'Final Score: {score}', True, (255, 255, 255))
        restart_text = self.font.render('Press R to Restart or ESC for Menu', True, (255, 255, 255))
        
        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(score_text, 
                        (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, 
                        (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

    def draw_pause_menu(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.title_font.render('PAUSED', True, (255, 255, 0))
        continue_text = self.font.render('Press P to Continue', True, (255, 255, 255))
        save_text = self.font.render('Press S to Save Game', True, (255, 255, 255))
        menu_text = self.font.render('Press ESC for Menu', True, (255, 255, 255))
        
        self.screen.blit(pause_text, 
                        (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(continue_text, 
                        (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(save_text, 
                        (SCREEN_WIDTH // 2 - save_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(menu_text, 
                        (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))

    def draw_main_menu(self, high_score=0, total_games=0):
        self.screen.fill(self.bg_color)
        
        title_text = self.title_font.render('SNAKE GAME', True, (0, 255, 0))
        start_text = self.font.render('Press ENTER to Start', True, (255, 255, 255))
        load_text = self.font.render('Press L to Load Game', True, (255, 255, 255))
        settings_text = self.font.render('Press C for Color Settings', True, (255, 255, 255))
        stats_text = self.font.render(f'High Score: {high_score} | Games: {total_games}', True, (200, 200, 200))
        quit_text = self.font.render('Press ESC to Quit', True, (255, 255, 255))
        
        self.screen.blit(title_text, 
                        (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        self.screen.blit(start_text, 
                        (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 220))
        self.screen.blit(load_text, 
                        (SCREEN_WIDTH // 2 - load_text.get_width() // 2, 270))
        self.screen.blit(settings_text, 
                        (SCREEN_WIDTH // 2 - settings_text.get_width() // 2, 320))
        self.screen.blit(stats_text, 
                        (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, 400))
        self.screen.blit(quit_text, 
                        (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 480))

    def draw_color_settings(self, bg_color, snake_color, food_color, selected_option=0):
        self.screen.fill((30, 30, 30))
        
        title_text = self.title_font.render('COLOR SETTINGS', True, (255, 255, 255))
        self.screen.blit(title_text, 
                        (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        
        options = [
            ('Background Color', bg_color),
            ('Snake Color', snake_color),
            ('Food Color', food_color)
        ]
        
        y_offset = 150
        for i, (name, color) in enumerate(options):
            prefix = '> ' if i == selected_option else '  '
            color_text = self.font.render(f'{prefix}{name}: RGB{color}', True, color)
            self.screen.blit(color_text, (SCREEN_WIDTH // 2 - color_text.get_width() // 2, y_offset))
            y_offset += 60
        
        preview_y = 350
        pygame.draw.rect(self.screen, bg_color, (SCREEN_WIDTH // 2 - 100, preview_y, 200, 100))
        pygame.draw.rect(self.screen, snake_color, (SCREEN_WIDTH // 2 - 80, preview_y + 40, 60, 20))
        pygame.draw.rect(self.screen, food_color, (SCREEN_WIDTH // 2 + 20, preview_y + 40, 20, 20))
        
        hint_text = self.font.render('Use +/- to adjust RGB values, UP/DOWN to select, ENTER to save', True, (200, 200, 200))
        back_text = self.font.render('Press ESC to go back without saving', True, (200, 200, 200))
        self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, 500))
        self.screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 540))

    def update(self):
        pygame.display.flip()
