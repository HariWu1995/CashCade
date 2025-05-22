import os
os.environ['SDL_VIDEO_CENTERED'] = '0'
# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

from pathlib import Path
work_dir = Path(__file__).resolve().parent
work_dir = str(work_dir).replace('\\', '/')

# HACK: hardcode
if work_dir.endswith('lib/library.zip'):
    work_dir = work_dir.replace('/lib/library.zip', '')
os.environ['WORKING_DIR'] = work_dir


import sys
import time
import traceback

import random
import pygame
import pyautogui

try:
    from src.ui import draw_block_game, draw_block_menu, draw_block_info
    from src.core import Player, Item, Button, ButtonM, GAME_GRID, GAME_STATES
    from src.config import WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, FPS, \
                            LIFETIME, LIFESPEED, STRENGTH, PROPERTY, MOVEMENT, \
                            FONT_NAME, FONT_SIZE, GRID_ROWS, GRID_COLS, BLACK
except Exception:
    print(traceback.format_exc())
    _ = input("Press ANY key to continue ... ")


work_dir = Path(work_dir)
asset_dir = work_dir / "assets"
font_dir = asset_dir / "fonts"

player_path = str(asset_dir / "casharacters/magikarp_orange.png")
esnemy_path = str(asset_dir / "casharacters/magikarp_gray.png")
elnemy_path = str(asset_dir / "casharacters/gyarados_red.png")
reward_path = str(asset_dir / "logo.png")
brand_path  = str(asset_dir / "Shinhan_Bank_logo.png")

button_ml_path = str(asset_dir / "misc/move_left.png")
button_mr_path = str(asset_dir / "misc/move_right.png")

button_ai_path = str(asset_dir / "misc/start.png")
button_ao_path = str(asset_dir / "misc/stop.png")

button_play_path = str(asset_dir / "misc/play.png")
button_exit_path = str(asset_dir / "misc/exit.png")


# Game constants
SPAWN_EVENT = pygame.USEREVENT + 1
SPAWN_INTERVAL = 250  # milliseconds


# Processing

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
        font_l = pygame.font.Font(str(font_dir / FONT_NAME), FONT_SIZE         )
        font_m = pygame.font.Font(str(font_dir / FONT_NAME), FONT_SIZE * 3 // 4)
        font_s = pygame.font.Font(str(font_dir / FONT_NAME), FONT_SIZE * 2 // 4)
    else:
        font_l = pygame.font.SysFont(FONT_NAME, FONT_SIZE         )
        font_m = pygame.font.SysFont(FONT_NAME, FONT_SIZE * 3 // 4)
        font_s = pygame.font.SysFont(FONT_NAME, FONT_SIZE * 2 // 4)

    # Timer
    clock = pygame.time.Clock()

    return window, (font_l, font_m, font_s), clock


def game(
    window, fonts, clock, 
    brand_img, 
    player,
    mvleft_button, mvright_button,
    all_in_button, all_out_button,
    game_exit_button,
):

    font_l, font_m, font_s = fonts
    font = font_l

    # Game variables
    player_lifetime = LIFETIME
    player_strength = STRENGTH
    player_property = PROPERTY
    player.reset()

    # Load sprites
    rewards = pygame.sprite.Group()
    sprites = pygame.sprite.Group(player, rewards)

    # Set spawn timer
    pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL)
    start_time = time.time()

    # Main
    running = True
    while running:

        # Displaying
        window.fill(BLACK)
        draw_block_game(window, font)

        # Recording
        draw_block_menu(window, font, player_lifetime, player_strength, player_property)
        window.blit(brand_img, (20, 25))

        # Information
        info_col = player.col - 1
        info_name = GAME_GRID[info_col]
        if info_name is not None:
            draw_block_info(window, font_m, info_name)

        game_exit_button.draw(window)

        # Time running out
        player_lifetime -= LIFESPEED

        if player.row == 7:
            player_lifetime -= GAME_STATES[GAME_GRID[player.col-1]]["lifespan"]

        if (player_lifetime <= 0) or (player_strength <= 0):
            print("Game Over!")
            running = False

        # Event Handling
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mvleft_button.is_clicked(mouse_pos):
                    mvleft_button.action()
                    player_strength -= MOVEMENT
                if mvright_button.is_clicked(mouse_pos):
                    mvright_button.action()
                    player_strength -= MOVEMENT
                if all_in_button.is_clicked(mouse_pos):
                    all_in_button.action()
                    player_strength -= MOVEMENT
                if all_out_button.is_clicked(mouse_pos):
                    all_out_button.action()
                    player_strength -= MOVEMENT
                if game_exit_button.is_clicked(mouse_pos):
                    running = False
                    break
            
            elif event.type == SPAWN_EVENT:
                for col, col_name in enumerate(GAME_GRID):
                    if col_name is None:
                        continue
                    col_state = GAME_STATES[col_name]

                    prob_property, \
                    prob_strength = col_state['probability']
                    if not isinstance(col_state['strength'], (list, tuple)):
                        value_strength = col_state['strength']
                    else:
                        value_strength = random.randint(*col_state['strength'])
                    if not isinstance(col_state['property'], (list, tuple)):
                        value_property = col_state['property']
                    else:
                        value_property = random.randint(*col_state['property'])

                    p_rand = random.random()
                    if p_rand < prob_property:
                        if value_property > 0:
                            item = Item(reward_path, col+1, 'reward', value_strength, value_property)
                        else:
                            continue
                    elif p_rand > (1. - prob_strength):
                        if value_strength > 0:
                            item = Item(reward_path, col+1, 'reward', value_strength, value_property)
                        elif value_strength < 0:
                            if value_strength <= -50:
                                enemy_path = elnemy_path
                                enemy_size = 'big'
                            else:
                                enemy_path = esnemy_path
                                enemy_size = 'small'
                            item = Item(enemy_path, col+1, 'risk', value_strength, value_property, size=enemy_size)
                        else:
                            continue
                    else:
                        continue

                    rewards.add(item)
                    sprites.add(item)

        # Update items
        for item in rewards:
            item.move()
            
            # Check collision with player
            if pygame.sprite.collide_rect(item, player):
                player_property += item.property
                player_strength += item.strength
                item.kill()

            # if item.row >= 7:
            #     item.kill()

        # Optional: draw grid lines
        # for x in range(COLS + 1):
        #     pygame.draw.line(window, (50, 50, 50), (x * cell_width, 0), (x * cell_width, screen_height))
        # for y in range(ROWS + 1):
        #     pygame.draw.line(window, (50, 50, 50), (0, y * cell_height), (screen_width, y * cell_height))

        sprites.draw(window)

        mvleft_button.draw(window)
        mvright_button.draw(window)

        all_in_button.draw(window)
        all_out_button.draw(window)

        # Timing
        pygame.display.flip()
        clock.tick(FPS)

    stop_time = time.time()
    print(f'\n\nGame happens in {stop_time-start_time} seconds')

    return player_lifetime, player_strength, player_property


def loop(window, fonts, clock):

    # Load brand logo
    brand_img = pygame.image.load(brand_path).convert_alpha()
    brand_img = pygame.transform.scale(brand_img, (225, 77))

    # Load player
    player = Player(player_path)

    # Load button images
    mvleft_button  = Button(button_ml_path, 4, lambda: player.move('left'))
    mvright_button = Button(button_mr_path, 6, lambda: player.move('right'))

    all_in_button  = Button(button_ai_path, 10, lambda: player.move('up'))
    all_out_button = Button(button_ao_path, 12, lambda: player.move('down'))

    game_play_button = ButtonM(button_play_path, (185, 86), position=(33, 770))
    game_exit_button = ButtonM(button_exit_path, (150, 70), position=(50, 850))

    # Record
    player_lifetime = LIFETIME
    player_strength = STRENGTH
    player_property = PROPERTY

    # Main
    playing = False
    quitting = False

    while not quitting:

        # Menu
        draw_block_menu(window, fonts[0], player_lifetime, player_strength, player_property)
        draw_block_game(window, fonts[0])

        window.blit(brand_img, (20, 25))

        game_play_button.draw(window)

        # Event Handling
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quitting = True
                break

            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            mouse_pos = pygame.mouse.get_pos()
            if game_play_button.is_clicked(mouse_pos):
                playing = True

        # Timing
        pygame.display.flip()
        clock.tick(FPS)

        # Game Playing
        if not playing:
            continue

        player_lifetime, \
        player_strength, \
        player_property = game(
            window, fonts, clock, 
            brand_img, player,
                mvleft_button, mvright_button,
                all_in_button, all_out_button, 
                game_exit_button,
        )
        playing = False

    return


if __name__ == "__main__":

    try:
        # Initialize
        window, fonts, clock = init()
        
        # Play
        loop(window, fonts, clock)

        # Stop
        pygame.quit()
        sys.exit()
    
    except Exception as e:
        print(traceback.format_exc())
        _ = input("Press ANY key to continue ... ")

