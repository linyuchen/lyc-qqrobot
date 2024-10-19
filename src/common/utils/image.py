import tempfile
from pathlib import Path

from PIL import Image


def merge_images(img_paths: list[Path]) -> Path:
    imgs = [Image.open(img_path) for img_path in img_paths]
    width = max([img.size[0] for img in imgs])
    height = sum([img.size[1] for img in imgs])
    merged_img = Image.new("RGB", (width, height), (255, 255, 255))
    y = 0
    for img in imgs:
        merged_img.paste(img, (0, y))
        y += img.size[1]
    merged_path = Path(tempfile.mktemp(suffix=".png"))
    merged_img.save(merged_path)
    return merged_path
