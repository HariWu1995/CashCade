import pygame

from ..config import MENU_WIDTH, GAME_WIDTH, PADDING, GRID_WIDTH, GRID_HEIGHT


GAME_COORDS = (MENU_WIDTH + PADDING * 3, PADDING)


class Item(pygame.sprite.Sprite):

    def __init__(self, image_path, column: int, kind: str,
                    strength_score: int = 0, property_score: int = 0, size: str = 'small'):
        
        super().__init__()
        self.kind = kind  # 'reward' or 'risk'
        self.strength = strength_score
        self.property = property_score

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (GRID_WIDTH // 1, GRID_HEIGHT // 1)) if size == "big" else \
                     pygame.transform.scale(self.image, (GRID_WIDTH // 3, GRID_HEIGHT // 3))

        self.rect = self.image.get_rect()

        # Start at first row
        self.row = 1
        self.col = column
        self.update_position()

    def update_position(self):
        self.col = max(1, self.col)
        self.col = min(18, self.col)

        self.row = max(1, self.row)
        self.row = min(7, self.row)

        col = self.col - 1
        row = self.row - 1
        self.rect.topleft = (GAME_COORDS[0] + col * GRID_WIDTH, 
                             GAME_COORDS[1] + row * GRID_HEIGHT)

    def move(self):
        # Move down one row per update
        self.update_position()

        # Remove if it leaves screen
        self.row += 1
        if self.row >= 8:
            self.kill()


