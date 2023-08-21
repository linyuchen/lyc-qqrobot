import os
import random

IMG_ROOT_PATH = "f:\\randomimg2"


def random_img():
    file_name = random.choice(os.listdir(IMG_ROOT_PATH))
    img_path = os.path.join(IMG_ROOT_PATH, file_name)
    return img_path
