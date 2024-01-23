import asyncio
import re
import tempfile
from pathlib import Path

import filetype
from meme_generator import Meme
from meme_generator.manager import get_memes

# 优化一些关键字和匹配方式
optimize = [
    {
        "key": "genshin_start",
        "keywords": ["启动", "原神启动"],
        "patterns": []
    }
]


def optimize_memes():
    for meme in get_memes():
        for opt in optimize:
            if meme.key == opt["key"]:
                meme.keywords = opt["keywords"]
                meme.patterns = opt["patterns"]


optimize_memes()


def generate(cli_text: str, images: list[Path]):
    cli_texts = cli_text.split(" ")
    input_meme_key = cli_texts[0]
    meme_object: Meme | None = None
    texts = []
    for meme in get_memes():
        if input_meme_key in meme.keywords:
            meme_object = meme
            texts = cli_texts[1:]
            break
        else:
            for pattern in meme.patterns:
                match_result = re.findall(pattern, cli_text)
                if match_result:
                    meme_object = meme
                    texts = match_result[0]
                    break
    if meme_object is None:
        return None

    max_texts = meme_object.params_type.max_texts
    min_texts = meme_object.params_type.min_texts
    if len(texts) < min_texts:
        return None
    if len(texts) > max_texts:
        texts = texts[:max_texts]

    max_images = meme_object.params_type.max_images
    min_images = meme_object.params_type.min_images
    if len(images) < min_images:
        return None
    if len(images) > max_images:
        images = images[:max_images]

    loop = asyncio.new_event_loop()
    images_bytes_io = loop.run_until_complete(meme_object(images=images, texts=texts or meme_object.params_type.default_texts))
    image_ext = filetype.guess_extension(images_bytes_io.getvalue())
    file_path = tempfile.mktemp(suffix=f".{image_ext}")
    file_path = Path(file_path)
    file_path.write_bytes(images_bytes_io.getvalue())
    return file_path


if __name__ == '__main__':
    # print(get_meme_keys())
    print(get_memes())
    # f = generate("许愿失败 我要对象", [])
    # print(f)
