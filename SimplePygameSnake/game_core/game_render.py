import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.game_settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    GRID_SIZE,
    MENU_FONT_SIZE,
    SCORE_FONT_SIZE,
    WHITE_COLOR,
    GRAY_COLOR
)


class GameRender:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, MENU_FONT_SIZE)
        self.font_medium = pygame.font.Font(None, SCORE_FONT_SIZE)
        self.font_small = pygame.font.Font(None, 20)
        try:
            self.font_chinese = pygame.font.SysFont('simhei', 24)
            self.font_chinese_large = pygame.font.SysFont('simhei', 36)
        except:
            self.font_chinese = self.font_medium
            self.font_chinese_large = self.font_large
    
    def clear_screen(self, color):
        self.screen.fill(color)
    
    def draw_snake(self, snake_body, color):
        for segment in snake_body:
            pygame.draw.rect(
                self.screen,
                color,
                pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE),
                1
            )
    
    def draw_food(self, position, color):
        pygame.draw.rect(
            self.screen,
            color,
            pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        )
    
    def draw_score(self, score):
        text = self.font_chinese.render(f"得分: {score}", True, WHITE_COLOR)
        self.screen.blit(text, (10, 10))
    
    def draw_game_over(self, score, high_score, is_new_high):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        title = self.font_chinese_large.render("游戏结束", True, WHITE_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(title, title_rect)
        score_text = self.font_chinese.render(f"本次得分: {score}", True, WHITE_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)
        high_text = self.font_chinese.render(f"最高分: {high_score}", True, WHITE_COLOR)
        high_rect = high_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(high_text, high_rect)
        if is_new_high:
            new_high_text = self.font_chinese.render("新纪录!", True, (255, 215, 0))
            new_high_rect = new_high_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(new_high_text, new_high_rect)
        hint = self.font_chinese.render("按 R 重新开始 | 按 ESC 返回菜单", True, GRAY_COLOR)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(hint, hint_rect)
    
    def draw_menu(self, high_score, total_games, total_time):
        self.screen.fill((30, 30, 50))
        title = self.font_chinese_large.render("贪吃蛇游戏", True, WHITE_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        stats_text = self.font_chinese.render(f"最高分: {high_score} | 游戏次数: {total_games} | 总时长: {total_time}秒", True, GRAY_COLOR)
        stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
        self.screen.blit(stats_text, stats_rect)
        menu_items = [
            ("按 SPACE 开始游戏", 250),
            ("按 S 读取存档", 300),
            ("按 C 画面设置", 350),
            ("按 ESC 退出游戏", 400)
        ]
        for text, y in menu_items:
            item = self.font_chinese.render(text, True, WHITE_COLOR)
            item_rect = item.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(item, item_rect)
    
    def draw_settings(self, color_util, selected_index):
        self.screen.fill((30, 30, 50))
        title = self.font_chinese_large.render("画面设置", True, WHITE_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        settings = [
            ("背景颜色", color_util.get_background_color()),
            ("蛇身颜色", color_util.get_snake_color()),
            ("食物颜色", color_util.get_food_color())
        ]
        for i, (name, color) in enumerate(settings):
            y = 120 + i * 80
            text = self.font_chinese.render(name, True, WHITE_COLOR)
            self.screen.blit(text, (100, y))
            pygame.draw.rect(self.screen, color, (300, y - 10, 100, 40))
            pygame.draw.rect(self.screen, WHITE_COLOR, (300, y - 10, 100, 40), 2)
            if i == selected_index:
                pygame.draw.rect(self.screen, (255, 255, 0), (90, y - 15, 320, 50), 3)
        color_list = color_util.get_color_list()
        start_x = 450
        for i, (name, color) in enumerate(color_list):
            x = start_x + (i % 7) * 50
            y = 120 + (i // 7) * 50
            pygame.draw.rect(self.screen, color, (x, y, 40, 40))
            pygame.draw.rect(self.screen, WHITE_COLOR, (x, y, 40, 40), 1)
        hint = self.font_chinese.render("上下键选择 | 左右键/点击色块更换颜色 | ESC返回", True, GRAY_COLOR)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(hint, hint_rect)
    
    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        pause_text = self.font_chinese_large.render("游戏暂停", True, WHITE_COLOR)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(pause_text, pause_rect)
        hint = self.font_chinese.render("按 P 继续 | 按 S 保存游戏 | 按 ESC 返回菜单", True, GRAY_COLOR)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(hint, hint_rect)
    
    def draw_save_success(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        text = self.font_chinese.render("存档成功!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
    
    def draw_load_failed(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        text = self.font_chinese.render("读取存档失败，开始新游戏", True, (255, 165, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
    
    def update(self):
        pygame.display.flip()
    
    def get_clock(self):
        return self.clock
    
    def get_screen(self):
        return self.screen
