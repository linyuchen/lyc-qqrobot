import base64
import io
import uuid
from pathlib import Path

import requests
from PIL import Image

import config
from msgplugins.chatgpt.chatgpt import chat

base_url = config.SD_HTTP_API + "/sdapi/v1/"

session = requests.Session()
session.timeout = 30


def trans2en(txt: str):
    prompt = "从现在开始你是一名基于输入描述的绘画AI提示词生成器，你会根据我输入的中文描述，生成符合主题的完整提示词。请注意，你生成后的内容服务于一个绘画AI，它只能理解具象的提示词而非抽象的概念，我将提供简短的描述，以便生成器可以为我提供准确的提示词。我希望生成的提示词能够包含人物的姿态、服装、妆容、情感表达和环境背景等细节，并且在必要时进行优化和重组以提供更加准确的描述，以便更好地服务于我的绘画AI，请严格遵守此条规则，也只输出翻译后的英文内容。请模仿结构示例生成准确提示词。示例输入：一位坐在床上的少女。 示例输出：1girl, sitting on, hand on own chest, head tilt, (indian_style:1.1), light smile, aqua eyes, (large breasts:1.2), blondehair, shirt, pleated_skirt, school uniform, (torn pantyhose:0.9), black garter belt, mary_janes, flower ribbon, glasses, looking at viewer, on bed,indoors,between legs. 请开始将下面的句子生成我需要的英文内容\n"
    result = chat("", prompt + txt)
    return result


def __api_get(url_path: str, params: dict = None):
    url = base_url + url_path
    resp = session.get(url, params=params)
    return resp.json()


def __api_post(url_path: str, data: dict = None):
    url = base_url + url_path
    resp = session.post(url, json=data)
    return resp.json()


def txt2img(txt: str, trans=True):
    """
    文字转图片
    :param txt: 文字
    :param trans: 是否翻译为英文
    :return: 图片的base64编码
    """
    if trans:
        txt = trans2en(txt)
    data = {
        "prompt": "(masterpiece:1,2), best quality, masterpiece, highres, original, extremely detailed wallpaper, perfect lighting,(extremely detailed CG:1.2)," + txt,
        "negative_prompt": "NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331), (morbid:1.21), (mutilated:1.21), (tranny:1.331), mutated hands, (poorly drawn hands:1.5), blurry, (bad anatomy:1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missing arms:1.331), (extra legs:1.331), (fused fingers:1.61051), (too many fingers:1.61051), (unclear eyes:1.331), lowers, bad hands, missing fingers, extra digit,bad hands, missing fingers, (((extra arms and legs))),NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331), (morbid:1.21), (mutilated:1.21), (tranny:1.331), mutated hands, (poorly drawn hands:1.5), blurry, (bad anatomy:1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missing arms:1.331), (extra legs:1.331), (fused fingers:1.61051), (too many fingers:1.61051), (unclear eyes:1.331), lowers, bad hands, missing fingers, extra digit,bad hands, missing fingers, (((extra arms and legs))),",
        "steps": 20,
    }
    r = __api_post("txt2img", data)
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
        image_path = Path(__file__).parent / (str(uuid.uuid4()) + ".png")
        image.save(image_path)
        # image.show()
        return str(image_path)


def __get_models():
    res = __api_get("sd-models")
    models = [m["model_name"] for m in res]
    models = "\n".join(models)
    return models


def __get_loras():
    res = __api_get("loras")
    # loras = [{"name": lora["name"], "frequency_tag": lora["metadata"]["ss_tag_frequency"].keys()} for lora in res]
    loras = [f'{lora["name"]}，标签：{"，".join(lora["metadata"]["ss_tag_frequency"].keys())}' for lora in res]
    loras = "\n\n".join(loras)
    return loras


def get_models():
    res = f"模型列表：\n{__get_models()}\n\nLora列表：\n{__get_loras()}"
    return res


def set_model(model_name: str):
    data = {
        "sd_model_checkpoint": model_name
    }
    r = __api_post("options", data)
    return r


if __name__ == '__main__':
    # print(txt2img("absurdres, 1girl, ocean, railing, white dress, sun hat,", False))
    # print(get_models())
    print(get_models())
    # print(set_model("二次元：AbyssOrangeMix2_sfw"))
    print(set_model("2.5D：Guofeng3 V32"))
