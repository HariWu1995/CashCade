import os
os.environ['SDL_VIDEO_CENTERED'] = '0'
# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

import sys
import time
from pathlib import Path

import random
import pygame
import pyautogui

from .ui import draw_block_game, draw_block_menu
from .core import Player, Item
from .config import (
    WINDOW_NAME, 
    WINDOW_WIDTH, WINDOW_HEIGHT, 
    LIFETIME, LIFESPEED, 
    STRENGTH, PROPERTY,
    FONT_NAME, FONT_SIZE, FPS,
    GRID_ROWS, GRID_COLS,
    LIFETIME, BLACK,
)


# Game constants
SPAWN_EVENT = pygame.USEREVENT + 1
SPAWN_INTERVAL = 1_000  # milliseconds

asset_dir = Path(__file__).resolve().parents[1] / "assets"

font_dir = asset_dir / "fonts"

player_path = str(asset_dir / "casharacters/magikarp_orange.png")
enemy_path  = str(asset_dir / "casharacters/magikarp_gray.png")
reward_path = str(asset_dir / "logo.png")


# Define per-column spawn probabilities (p_reward, p_risk)
# Example: higher reward chance in middle columns
column_probs = [(0.05, 0.02) for _ in range(GRID_COLS)]
for i in range(GRID_COLS):
    column_probs[i] = (0.02 + 0.03 * (1 - abs(i - GRID_COLS//2) / (GRID_COLS//2)), 0.02)
# print(column_probs)


def init():
    pygame.init()

    # Screen
    pygame.display.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(WINDOW_NAME)

    # info = pygame.display.Info()
    # print(info)

    # Font
    pygame.font.init()
    if FONT_NAME.endswith('.ttf'):
        font = pygame.font.Font(str(font_dir / FONT_NAME), FONT_SIZE)
    else:
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    # Timer
    clock = pygame.time.Clock()

    return window, font, clock


def main(window, font, clock):

    # Game variables
    player_lifetime = LIFETIME
    player_strength = STRENGTH
    player_property = PROPERTY

    # Load sprites
    player = Player(player_path)
    rewards = pygame.sprite.Group()
    sprites = pygame.sprite.Group(player, rewards)

    # Set spawn timer
    pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL)

    start_time = time.time()
    running = True
    while running:

        # Displaying
        window.fill(BLACK)
        draw_block_game(window, font)

        # Time running out
        player_lifetime -= LIFESPEED
        if player_lifetime <= 0:
            print("Game Over!")
            running = False

        # Event Handling
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move('left')
                elif event.key == pygame.K_RIGHT:
                    player.move('right')
            
            elif event.type == SPAWN_EVENT:
                # For each column, attempt spawn
                for col in range(GRID_COLS):
                    p_reward, p_risk = column_probs[col]
                    r = random.random()
                    if r < p_reward:
                        item = Item(reward_path, col, 'reward')
                        rewards.add(item)
                        sprites.add(item)
                    elif r < p_reward + p_risk:
                        item = Item(enemy_path, col, 'risk')
                        rewards.add(item)
                        sprites.add(item)

        # Update items
        for item in rewards:
            item.move()
            # Check collision with player
            if pygame.sprite.collide_rect(item, player):
                if item.kind == 'reward':
                    player_property += 1
                else:
                    player_property -= 1
                item.kill()

        # Optional: draw grid lines
        # for x in range(COLS + 1):
        #     pygame.draw.line(window, (50, 50, 50), (x * cell_width, 0), (x * cell_width, screen_height))
        # for y in range(ROWS + 1):
        #     pygame.draw.line(window, (50, 50, 50), (0, y * cell_height), (screen_width, y * cell_height))

        sprites.draw(window)

        # Draw record
        draw_block_menu(window, font, player_lifetime, player_strength, player_property)

        # Timing
        pygame.display.flip()
        clock.tick(FPS)

    stop_time = time.time()
    print(f'\n\nGame happens in {stop_time-start_time} seconds')

    return



if __name__ == "__main__":

    # Initialize
    window, font, clock = init()
    
    # Play
    main(window, font, clock)

    # Stop
    pygame.quit()
    sys.exit()

