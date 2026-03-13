import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.game_settings import SCREEN_WIDTH, SCREEN_HEIGHT
from game_core.game_logic import Game, main_menu, color_settings_screen, show_stats_screen

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("贪吃蛇游戏")
    
    current_state = "MENU"
    
    while True:
        if current_state == "MENU":
            current_state = main_menu(screen)
        elif current_state == "PLAY":
            game = Game(screen)
            current_state = game.run()
        elif current_state == "COLOR_SETTINGS":
            current_state = color_settings_screen(screen)
        elif current_state == "STATS":
            current_state = show_stats_screen(screen)
        elif current_state == "QUIT":
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
