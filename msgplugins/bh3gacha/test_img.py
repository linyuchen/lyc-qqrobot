import os
from PIL import Image

current_path = os.path.dirname(__file__)
img_path = os.path.join(current_path, "test-imgs")

img_bg = Image.open(os.path.join(img_path, "bg.png"))
img2 = Image.open(img_path).resize((40, 30))

img_bg.paste(img2, (10, 20))
img_bg.save(os.path.join(current_path, "new.png"))
