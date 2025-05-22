import time
import pygame

from ..config import (
    MENU_BACKGROUND, PADDING, 
    MENU_WIDTH, MENU_HEIGHT,
    MENU_TEXT_LIFETIME, 
    MENU_TEXT_STRENGTH, 
    MENU_TEXT_PROPERTY,
)


def draw_block(window, font, plifetime, pstrength, pproperty):
    pygame.draw.rect(window, MENU_BACKGROUND, 
                            (PADDING             , PADDING, 
                             PADDING + MENU_WIDTH, PADDING + MENU_HEIGHT))

    # Calculate remaining time
    # elapsed_time = time.time() - start_time
    # remaining_time = max(0, int(LIFETIME - elapsed_time))

    # Render display texts
    lftime_text = font.render(f"Lifespan: {plifetime}", True, MENU_TEXT_LIFETIME)
    health_text = font.render(f"Strength: {pstrength}", True, MENU_TEXT_STRENGTH)
    reward_text = font.render(f"Property: {pproperty}", True, MENU_TEXT_PROPERTY)

    # Blit texts
    window.blit(lftime_text, (20, 200))
    window.blit(health_text, (20, 250))
    window.blit(reward_text, (20, 300))

