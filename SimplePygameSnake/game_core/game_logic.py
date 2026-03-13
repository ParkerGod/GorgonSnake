import json
import os
import time
import pygame

from config.game_settings import SAVE_FILE_PATH, SNAKE_SPEED
from game_core.snake_control import Snake, Food
from game_core.game_render import GameRenderer, CHINESE_FONT
from utils.util_db import init_database, get_game_stats, save_game_result
from utils.util_color import save_colors_config, get_all_color_names, get_color_by_name, load_colors_config

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.config = load_colors_config()
        self.renderer = GameRenderer(screen, self.config)
        self.snake = Snake()
        self.food = Food(self.snake.get_body())
        self.score = 0
        self.game_over = False
        self.start_time = time.time()
        self.running = True
        
        init_database()
    
    def reset_game(self):
        self.snake.reset()
        self.food.spawn(self.snake.get_body())
        self.score = 0
        self.game_over = False
        self.start_time = time.time()
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.game_over:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_m:
                    return "MENU"
            else:
                if event.key == pygame.K_UP:
                    self.snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction('RIGHT')
                elif event.key == pygame.K_s:
                    self.save_game()
                elif event.key == pygame.K_l:
                    self.load_game()
                elif event.key == pygame.K_p:
                    self.pause_game()
        return None
    
    def pause_game(self):
        paused = True
        font = pygame.font.Font(CHINESE_FONT, 72)
        text = font.render("游戏暂停", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.update()
        
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    paused = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                    elif event.key == pygame.K_q:
                        self.running = False
                        paused = False
    
    def update(self):
        if not self.game_over:
            self.snake.move()
            
            if self.snake.check_collision_with_boundary() or self.snake.check_collision_with_self():
                self.game_over = True
                play_time = time.time() - self.start_time
                save_game_result(self.score, play_time)
            
            head_pos = self.snake.get_head_position()
            food_pos = self.food.get_position()
            
            if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
                self.score += 10
                self.snake.grow()
                self.food.spawn(self.snake.get_body())
    
    def render(self):
        self.renderer.clear_screen()
        self.renderer.draw_snake(self.snake.get_body())
        self.renderer.draw_food(self.food.get_position())
        self.renderer.draw_score(self.score)
        
        if self.game_over:
            self.renderer.draw_game_over()
        
        self.renderer.update_display()
    
    def save_game(self):
        os.makedirs(os.path.dirname(SAVE_FILE_PATH), exist_ok=True)
        game_state = {
            "snake_body": self.snake.get_body(),
            "snake_direction": self.snake.direction,
            "food_position": self.food.get_position(),
            "score": self.score
        }
        with open(SAVE_FILE_PATH, 'w') as f:
            json.dump(game_state, f)
    
    def load_game(self):
        if os.path.exists(SAVE_FILE_PATH):
            with open(SAVE_FILE_PATH, 'r') as f:
                game_state = json.load(f)
            self.snake.set_state(game_state["snake_body"], game_state["snake_direction"])
            self.food.set_position(game_state["food_position"][0], game_state["food_position"][1])
            self.score = game_state["score"]
            self.game_over = False
            self.start_time = time.time()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                result = self.handle_input(event)
                if result == "MENU":
                    return "MENU"
            
            self.update()
            self.render()
            self.clock.tick(SNAKE_SPEED)
        
        return "QUIT"

def show_stats_screen(screen):
    play_count, highest_score, total_time = get_game_stats()
    config = load_colors_config()
    renderer = GameRenderer(screen, config)
    
    showing = True
    while showing:
        renderer.clear_screen()
        renderer.draw_stats(play_count, highest_score, total_time)
        renderer.update_display()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                showing = False
    return "MENU"

def color_settings_screen(screen):
    config = load_colors_config()
    color_names = [
        get_color_name(config["background"]),
        get_color_name(config["snake"]),
        get_color_name(config["food"])
    ]
    
    all_colors = get_all_color_names()
    current_selection = 0
    selected_index = [
        all_colors.index(color_names[0]) if color_names[0] in all_colors else 0,
        all_colors.index(color_names[1]) if color_names[1] in all_colors else 0,
        all_colors.index(color_names[2]) if color_names[2] in all_colors else 0
    ]
    
    renderer = GameRenderer(screen, config)
    
    running = True
    while running:
        renderer.clear_screen()
        renderer.draw_color_settings(current_selection, color_names, selected_index)
        renderer.update_display()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    current_selection = (current_selection - 1) % 3
                elif event.key == pygame.K_DOWN:
                    current_selection = (current_selection + 1) % 3
                elif event.key == pygame.K_LEFT:
                    selected_index[current_selection] = (selected_index[current_selection] - 1) % len(all_colors)
                    color_names[current_selection] = all_colors[selected_index[current_selection]]
                    update_config(config, current_selection, get_color_by_name(color_names[current_selection]))
                    renderer.config = config
                elif event.key == pygame.K_RIGHT:
                    selected_index[current_selection] = (selected_index[current_selection] + 1) % len(all_colors)
                    color_names[current_selection] = all_colors[selected_index[current_selection]]
                    update_config(config, current_selection, get_color_by_name(color_names[current_selection]))
                    renderer.config = config
                elif event.key == pygame.K_RETURN:
                    save_colors_config(config["background"], config["snake"], config["food"])
    
    return "MENU"

def get_color_name(color_value):
    from config.game_settings import COLOR_OPTIONS
    for color in COLOR_OPTIONS:
        if color["value"] == color_value:
            return color["name"]
    return "自定义"

def update_config(config, selection, color_value):
    if selection == 0:
        config["background"] = color_value
    elif selection == 1:
        config["snake"] = color_value
    elif selection == 2:
        config["food"] = color_value

def handle_menu_selection(selected, options):
    actions = ["PLAY", "COLOR_SETTINGS", "STATS", "QUIT"]
    if selected < len(actions):
        return actions[selected]
    return "MENU"

def main_menu(screen):
    config = load_colors_config()
    renderer = GameRenderer(screen, config)
    options = ["开始游戏", "颜色设置", "游戏统计", "退出游戏"]
    selected = 0
    clock = pygame.time.Clock()
    button_rects = []
    
    running = True
    while running:
        renderer.clear_screen()
        button_rects = renderer.draw_menu(options, selected)
        renderer.update_display()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return handle_menu_selection(selected, options)
            if event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        selected = i
                        break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            return handle_menu_selection(i, options)
        
        clock.tick(30)
