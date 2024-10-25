import pygame
from game.assets_loader import load_assets
from game.game_logic import startScreen

def main():
    pygame.init()
    pygame.mixer.init()

    images, sounds, fonts, background_path = load_assets()

    levels = []
    level_index = -1

    startScreen(level_index, levels, images, sounds, fonts, background_path)

if __name__ == "__main__":
    main()