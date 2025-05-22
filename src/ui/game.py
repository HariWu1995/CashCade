from pathlib import Path
from PIL import Image

import pygame
import pyautogui

from ..core import Button
from ..config import (
    MENU_WIDTH, MENU_HEIGHT, FPS,
    GAME_WIDTH, GAME_HEIGHT, PADDING,
    GAME_BACKGROUND, GAME_TEXT_COLOR,
)

import os

work_dir = os.environ.get('WORKING_DIR', None)
if work_dir is None:
    work_dir = Path(__file__).resolve().parents[2]
else:
    work_dir = Path(work_dir)

asset_dir = work_dir / "assets"

background_path = asset_dir / "backgrounds/full_background.gif"
character_path  = asset_dir / "casharacters/magikarp_orange.png"
competitor_path = asset_dir / "casharacters/magikarp_gray.png"

info_button_path  = asset_dir / "misc/info.png"
start_button_path = asset_dir / "misc/golden-start.png"


BACKGROUND_GIF = Image.open(background_path)
BACKGROUND_INDEX = 0
BACKGROUND_FRAMES = []
try:
    while True:
        frame = BACKGROUND_GIF.copy().convert("RGB")
        frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
        BACKGROUND_FRAMES.append(frame)
        BACKGROUND_GIF.seek(len(BACKGROUND_FRAMES))  # Go to next frame
except EOFError:
    pass  # Done reading all frames


game_coordinates = (
    MENU_WIDTH + PADDING * 3, PADDING, 
    GAME_WIDTH + PADDING * 3, PADDING + GAME_HEIGHT,
)


def draw_block(window, font):

    # Simulate a game area with a background color
    pygame.draw.rect(window, GAME_BACKGROUND, game_coordinates)

    global BACKGROUND_INDEX
    BACKGROUND_INDEX += 1
    BACKGROUND_INDEX = BACKGROUND_INDEX % len(BACKGROUND_FRAMES)
    window.blit(BACKGROUND_FRAMES[BACKGROUND_INDEX], game_coordinates[:2])

    # [Optional] Mouse position
    # mouse_x, mouse_y = pyautogui.position()
    # mpos_text = font.render(f"Mouse: ({mouse_x}, {mouse_y})", True, GAME_TEXT_COLOR)
    # window.blit(mpos_text, (30, 700))


