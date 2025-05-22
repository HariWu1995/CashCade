import pygame

from ..config import MENU_WIDTH, GAME_WIDTH, PADDING, GRID_WIDTH, GRID_HEIGHT
from .zones import GAME_GRID


GAME_COLUMNS = [(i+1) for i in range(len(GAME_GRID)) if GAME_GRID[i] is not None]
GAME_COORDS = (MENU_WIDTH + PADDING * 3, PADDING)


class Player(pygame.sprite.Sprite):

    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (GRID_WIDTH, GRID_HEIGHT))

        self.rect = self.image.get_rect()
        self.reset()

        self.image_l2r = self.image
        self.image_r2l = pygame.transform.flip(self.image, True, False)

    def reset(self):
        # Start at bottom row (row index 8)
        self.row = 8
        self.col = 2
        self.update_position()

    def update_position(self):
        self.col = max(1, self.col)
        self.col = min(18, self.col)

        self.row = max(7, self.row)
        self.row = min(8, self.row)

        col = self.col - 1
        row = self.row - 1
        self.rect.topleft = (GAME_COORDS[0] + col * GRID_WIDTH, 
                             GAME_COORDS[1] + row * GRID_HEIGHT)

    def move(self, direction: str):

        if direction in ['left','right'] and self.row == 7:
            if self.col == 2:
                return
            if self.col in [4, 7, 11, 14] and direction == 'left':
                return
            if self.col in [5, 9, 12, 17] and direction == 'right':
                return            

        if direction in ['up','down'] and self.col not in GAME_COLUMNS:
            return

        if direction == 'left':
            self.col -= 1
            self.image = self.image_r2l

        elif direction == 'right':
            self.col += 1
            self.image = self.image_l2r

        elif direction == 'up':
            self.row -= 1

        elif direction == 'down':
            self.row += 1

        self.update_position()


