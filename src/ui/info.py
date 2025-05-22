import time
import pygame

from ..core import GAME_STATES
from ..config import (
    MENU_BACKGROUND, PADDING, 
    MENU_WIDTH, MENU_HEIGHT,
    MENU_TEXT_LIFETIME, 
    MENU_TEXT_STRENGTH, 
    MENU_TEXT_PROPERTY,
)


def draw_block(window, font, info_name: str):

    info_dict = GAME_STATES[info_name]

    # Render display texts
    titleH_text = font.render(f"Strategy:", True, MENU_TEXT_STRENGTH)
    titleC_text = font.render(f"    {info_name}", True, MENU_TEXT_STRENGTH)

    timeH_text = font.render(f"Time-cost:", True, MENU_TEXT_LIFETIME)
    timeC_text = font.render(f"    Value: -{info_dict['lifespan']}", True, MENU_TEXT_LIFETIME)

    propH_text = font.render(f"Property:", True, MENU_TEXT_PROPERTY)
    propV_text = font.render(f"   Value: {info_dict['property']}", True, MENU_TEXT_PROPERTY)
    propP_text = font.render(f"   Prob.: {info_dict['probability'][0] * 100}", True, MENU_TEXT_PROPERTY)

    healthH_text = font.render(f"Strength:", True, MENU_TEXT_STRENGTH)
    healthV_text = font.render(f"   Value: {info_dict['strength']}", True, MENU_TEXT_STRENGTH)
    healthP_text = font.render(f"   Prob.: {info_dict['probability'][1] * 100}", True, MENU_TEXT_STRENGTH)

    # Blit texts
    window.blit(titleH_text, (30, 400))
    window.blit(titleC_text, (30, 430))

    window.blit(timeH_text, (30, 470))
    window.blit(timeC_text, (30, 500))
    
    window.blit(propH_text, (30, 540))
    window.blit(propV_text, (30, 570))
    window.blit(propP_text, (30, 600))
    
    window.blit(healthH_text, (30, 640))
    window.blit(healthV_text, (30, 670))
    window.blit(healthP_text, (30, 700))

