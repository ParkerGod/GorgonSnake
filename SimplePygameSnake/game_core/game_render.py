import pygame
import os
from config.game_settings import GRID_SIZE, TEXT_COLOR, MENU_COLOR

def get_chinese_font():
    font_paths = [
        'C:/Windows/Fonts/msyh.ttf',
        'C:/Windows/Fonts/simhei.ttf',
        'C:/Windows/Fonts/simsun.ttc',
    ]
    for path in font_paths:
        if os.path.exists(path):
            return path
    return pygame.font.get_default_font()

CHINESE_FONT = get_chinese_font()

class GameRenderer:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.font_small = pygame.font.Font(CHINESE_FONT, 24)
        self.font_medium = pygame.font.Font(CHINESE_FONT, 36)
        self.font_large = pygame.font.Font(CHINESE_FONT, 72)
    
    def clear_screen(self):
        self.screen.fill(self.config["background"])
    
    def draw_snake(self, snake_body):
        for segment in snake_body:
            pygame.draw.rect(
                self.screen,
                self.config["snake"],
                pygame.Rect(segment[0], segment[1], GRID_SIZE - 2, GRID_SIZE - 2)
            )
    
    def draw_food(self, food_pos):
        pygame.draw.rect(
            self.screen,
            self.config["food"],
            pygame.Rect(food_pos[0], food_pos[1], GRID_SIZE - 2, GRID_SIZE - 2)
        )
    
    def draw_score(self, score):
        score_text = self.font_medium.render(f"得分: {score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
    
    def draw_game_over(self):
        text1 = self.font_large.render("游戏结束!", True, TEXT_COLOR)
        text2 = self.font_medium.render("按 R 重新开始 或 Q 退出", True, TEXT_COLOR)
        text3 = self.font_medium.render("按 M 返回主菜单", True, TEXT_COLOR)
        
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        
        self.screen.blit(text1, (center_x - text1.get_width() // 2, center_y - 100))
        self.screen.blit(text2, (center_x - text2.get_width() // 2, center_y))
        self.screen.blit(text3, (center_x - text3.get_width() // 2, center_y + 50))
    
    def draw_menu(self, options, selected_index, title="贪吃蛇游戏"):
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        button_rects = []
        
        title_text = self.font_large.render(title, True, TEXT_COLOR)
        self.screen.blit(title_text, (center_x - title_text.get_width() // 2, center_y - 150))
        
        for i, option in enumerate(options):
            color = TEXT_COLOR if i == selected_index else MENU_COLOR
            option_text = self.font_medium.render(option, True, color)
            text_rect = option_text.get_rect(center=(center_x, center_y - 50 + i * 50))
            button_rect = pygame.Rect(text_rect.x - 20, text_rect.y - 5, text_rect.width + 40, text_rect.height + 10)
            if i == selected_index:
                pygame.draw.rect(self.screen, (80, 80, 80), button_rect)
            self.screen.blit(option_text, text_rect)
            button_rects.append(button_rect)
        
        return button_rects
    
    def draw_color_settings(self, current_selection, color_names, selected_index):
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        
        title_text = self.font_large.render("颜色设置", True, TEXT_COLOR)
        self.screen.blit(title_text, (center_x - title_text.get_width() // 2, 50))
        
        options = ["背景颜色", "蛇身颜色", "食物颜色"]
        for i, option in enumerate(options):
            color = TEXT_COLOR if i == current_selection else MENU_COLOR
            text = self.font_medium.render(f"{option}: {color_names[i]}", True, color)
            self.screen.blit(text, (center_x - text.get_width() // 2, 150 + i * 60))
        
        help_text = self.font_small.render("方向键选择颜色, 回车确认, ESC 返回", True, TEXT_COLOR)
        self.screen.blit(help_text, (center_x - help_text.get_width() // 2, center_y + 150))
    
    def draw_stats(self, play_count, highest_score, total_time):
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        
        title_text = self.font_large.render("游戏统计", True, TEXT_COLOR)
        self.screen.blit(title_text, (center_x - title_text.get_width() // 2, 100))
        
        stats = [
            f"游玩次数: {play_count}",
            f"最高得分: {highest_score}",
            f"总游戏时长: {total_time:.1f} 秒"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font_medium.render(stat, True, TEXT_COLOR)
            self.screen.blit(text, (center_x - text.get_width() // 2, 200 + i * 60))
        
        back_text = self.font_medium.render("按任意键返回", True, TEXT_COLOR)
        self.screen.blit(back_text, (center_x - back_text.get_width() // 2, center_y + 100))
    
    def update_display(self):
        pygame.display.update()
