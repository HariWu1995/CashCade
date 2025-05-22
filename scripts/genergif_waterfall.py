import os
from glob import glob
from tqdm import tqdm

from PIL import Image
from pathlib import Path


image_folder = Path(__file__).resolve().parents[1] / "assets/animations"
image_pattern = "waterfall_high_blue_0*.png"
image_path = str(image_folder / image_pattern).replace('\\', '/')
print(image_path)


frames = [Image.open(i).resize((66*16, 180*16), Image.BILINEAR) for i in glob(image_path)]
# frames = [i.resize() for img in frames]
print(len(frames))


# frames = []
# for img in frames:
#     width, height = img.size
#     patches = [img.crop((i * (width // 4), 0, (i + 1) * (width // 4), height)) for i in range(4)]
#     frames.extend(patches)


frame_one = frames[0]
frame_one.save((image_folder / "waterfall_high_blue_x16.gif"), 
                format="GIF", append_images=frames, 
                save_all=True, duration=100, loop=0)

