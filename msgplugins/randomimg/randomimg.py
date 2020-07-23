import os
import random

IMG_ROOT_PATH = "G:\\randomimg"


def random_img():
    file_name = random.choice(os.listdir(IMG_ROOT_PATH))
    return os.path.join(IMG_ROOT_PATH, file_name)
