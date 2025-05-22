from PIL import Image
from PIL.Image import Image as ImageClass
import pygame

import cv2
import numpy as np


def convert_pil_image(pil_image: ImageClass):
    image_mode = pil_image.mode
    image_size = pil_image.size
    image_data = pil_image.tobytes()

    image = pygame.image.fromstring(image_data, image_size, image_mode)
    return image


def convert_np_image(
    np_image: np.ndarray, 
    color_channels: int = 3,
    rotate_clockwise: int = 0,
    flip_left_right: bool = False,
    flip_up_down: bool = False,
):
    image = np_image[:, :, :color_channels]

    # resize
    # image = cv2.resize(image, dsize=(0,0), fx=WIDTH/1600, fy=HEIGHT/860, 
    #                     interpolation=cv2.INTER_CUBIC)

    # rotate clock-wise
    if rotate_clockwise == 1:
        image_arr = np.rot90(image, k=1, axes=(1,0))

    # rotate counter-clock-wise
    elif rotate_clockwise == -1:
        image_arr = np.rot90(image, k=1, axes=(0,1))
    
    # flip horizontally
    if flip_left_right:
        image_arr = np.fliplr(image_arr) 

    # flip vertically
    if flip_up_down:
        image_arr = np.flipud(image_arr) 

    image_arr = pygame.surfarray.make_surface(image_arr)
    return image_arr


def transform_coordinate(position, new_W, new_H, old_W=1920, old_H=1080):
    """
    Corresponding to step-by-step of function `convert_np_image`
    """
    position_w, position_h = position
    # print(position_w, position_h)

    # Apply to rotate clockwise
    M = cv2.getRotationMatrix2D(center=(old_W//2, old_H//2), angle=-90, scale=1.0)

    cosine = np.abs(M[0, 0])
    sine   = np.abs(M[0, 1])

    position_w = int(old_H * sine   + old_W * cosine)
    position_h = int(old_H * cosine + old_W * sine  )
    # print(position_w, position_h)

    # Apply to resize
    position_w *= (new_W // old_W)
    position_h *= (new_H // old_H)
    # print(position_w, position_h)

    # Apply to flip horizontally
    position_w = new_W - position_w

    # print(position_w, position_h)
    return position_w, position_h

