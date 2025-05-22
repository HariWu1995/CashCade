import os
from glob import glob
from tqdm import tqdm

from PIL import Image
from pathlib import Path


# Source: https://www.slynyrd.com/blog/2018/10/12/pixelblog-10-water-in-motion
image_folder = Path(__file__).resolve().parents[1] / "assets/animations"
image_panel = image_folder / "waterfall_high_pastel.png"
image_path = str(image_panel).replace('\\', '/')
print(image_path)


panel = Image.open(image_path)#.crop((4, 452, 4, 218))
width, height = panel.size
width = width // 6

frames = []
for i in range(6):
    frame = panel.crop((i * width, 0, (i+1) * width, height))

    # Translation
    k = i // 2
    temp = Image.new("RGB", (width + k, height), (0, 0, 0))
    temp.paste(frame, (k, 0))
    frame = temp.crop((0, 0, width, height))

    # Upscaling
    frame = frame.crop((4, 4, width - 4, height - 4))
    frame = frame.resize((width * 24, height * 24), Image.BILINEAR)
    frames.append(frame)


# Transparency: Background = (47, 33, 59) = #2F213B
bg_color = (47, 33, 59)
frames_rgba = []
for frame in frames:
    frame_rgba = frame.convert('RGBA')
    frame_data = frame_rgba.getdata()

    new_data = []
    for d in tqdm(frame_data):
        if d[:3] == bg_color:
            # Replace matching color with full transparency
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(d)

    frame_rgba.putdata(new_data)
    frames_rgba.append(frame_rgba)


# Saving
frame_one = frames_rgba[0]
frame_one.save((image_folder / "waterfall_high_pastel_x24_rgba.gif"), 
                format="GIF", append_images=frames_rgba, 
                save_all=True, duration=100, loop=0)

