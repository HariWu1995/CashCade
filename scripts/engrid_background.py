import os
import sys

from glob import glob
from tqdm import tqdm
from pathlib import Path

import imageio as iio
from PIL import Image, ImageDraw


working_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(working_dir))

# Configure
from src.config import GAME_WIDTH, GAME_HEIGHT


image_folder = working_dir / "assets/backgrounds"
background_path = str(image_folder / "full_background.png")


# Load image
background = Image.open(background_path)
drawer = ImageDraw.Draw(background)


# Grid
img_width, img_height = background.size

grid_width = 18
grid_height = 9

line_color = (255, 0, 0)
line_width = 1

cell_width  = img_width  // grid_width
cell_height = img_height // grid_height


# Draw vertical lines
for i in range(1, grid_width):
    x = int(i * cell_width)
    drawer.line([(x, 0), (x, img_height)], fill=line_color, width=line_width)

# Draw horizontal lines
for j in range(1, grid_height):
    y = int(j * cell_height)
    drawer.line([(0, y), (img_width, y)], fill=line_color, width=line_width)


# Save
background.save((image_folder / "grid_background.png"))

