import pygame

from ..config import MENU_WIDTH, GAME_WIDTH, PADDING, GRID_WIDTH, GRID_HEIGHT


GAME_COORDS = (MENU_WIDTH + PADDING * 3, PADDING)


class ButtonM:

    def __init__(self, image_path, image_size, position):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, image_size)
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Button:

    def __init__(self, image_path, column: int, action):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (GRID_WIDTH*2, GRID_HEIGHT))
        self.action = action

        # last bottom row
        self.row = 9
        self.col = column

        self.rect = self.image.get_rect()
        self.update_position()

    def update_position(self):
        self.col = max(1, self.col)
        self.col = min(18, self.col)

        self.row = max(1, self.row)
        self.row = min(9, self.row)

        col = self.col - 1
        row = self.row - 1
        self.rect.topleft = (GAME_COORDS[0] + col * GRID_WIDTH, 
                             GAME_COORDS[1] + row * GRID_HEIGHT)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class ButtonV2(pygame.sprite.Sprite):
    
    def __init__(self, window, image_arr, position, activate=True):
        
        super().__init__()

        self.image = pygame.surfarray.make_surface(image_arr)
        self.activate = activate

        position_w, position_h = position
        # print(position_w, position_h)
        
        # position_w = int(position_w * WIDTH  / 1920)
        # position_h = int(position_h * HEIGHT / 1080)
        # print(position_w, position_h)

        self.position = (position_w, position_h)
        
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        # print(self.rect)

        window.blit(self.image, self.position)

