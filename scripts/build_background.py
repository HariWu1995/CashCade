import os
import sys

from glob import glob
from tqdm import tqdm
from pathlib import Path

import imageio as iio
from PIL import Image
from PIL.ImageSequence import Iterator as ImageIterator


working_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(working_dir))

# Configure
from src.config import GAME_WIDTH, GAME_HEIGHT, GRID_HEIGHT


image_folder = working_dir / "assets/backgrounds"
bg_top_path = str(image_folder / "waterfall-lanes.gif")
bg_bot_path = str(image_folder / "water-pool.gif")


# Load GIF
bg_top_gif = Image.open(bg_top_path)
bg_bot_gif = Image.open(bg_bot_path)


# Extract frames + Resize
bg_top_frames = [frame.copy().resize((768, 512)) for frame in ImageIterator(bg_top_gif)]  # 22
bg_bot_frames = [frame.copy().resize((768, 168)) for frame in ImageIterator(bg_bot_gif)]  # 4


# Ensure both GIFs have the same number of frames

# min_frames = min(len(bg_top_frames), len(bg_bot_frames))
# bg_top_frames = bg_top_frames[:min_frames]
# bg_bot_frames = bg_bot_frames[:min_frames]

bg_top_frames = bg_top_frames[:1] + bg_top_frames + bg_top_frames[-1:]
bg_bot_frames = bg_bot_frames[0:1] * 6 \
              + bg_bot_frames[1:2] * 6 \
              + bg_bot_frames[2:3] * 6 \
              + bg_bot_frames[3:4] * 6
# bg_bot_frames = bg_bot_frames * 6


# Concat horizontal
frames = []

for f1, f2 in zip(bg_top_frames, bg_bot_frames):

    # Convert to RGBA for consistent handling
    f1 = f1.convert("RGBA")
    f2 = f2.convert("RGBA")

    # HACK: Modify bottom frame

    pixels_new = []
    pixels_old = f2.getdata()
    for d in tqdm(pixels_old):
        # if d[3] == 0:
        #     pixels_new.append((65, 159, 204, 255))
        # else:
        #     pixels_new.append(d)
        pixels_new.append((65, 159, 204, 255))
    f2.putdata(pixels_new)

    f1 = f1.crop((10, 0, 760, 512)).resize((768, GRID_HEIGHT*7))
    # f2 = f2.crop((61, 0, 768, 168)).resize((768, 256))

    # Concatenate
    new_width = max(f1.width, f2.width)
    new_height = f1.height + f2.height

    new_image = Image.new("RGBA", size=(new_width, new_height), color=(65, 159, 204, 255))
    new_image.paste(f1, (0, 0))
    # new_image.paste(f2, (0, f1.height))
    # new_image = new_image.resize((1536, 768))
    new_image = new_image.resize((GAME_WIDTH, GAME_HEIGHT))

    frames.append(new_image)


# Save
frame_one = frames[0]
frame_one.save((image_folder / "full_background.png"))
frame_one.save((image_folder / "full_background.gif"), 
                format="GIF", append_images=frames, 
                save_all=True, duration=100, loop=0)

