import abc
import re
from typing import Callable

import requests

from msgplugins.chatgpt import chat


class AIDrawBase(metaclass=abc.ABCMeta):
    base_prompt = "(masterpiece:1,2), best quality, highres, original, extremely detailed wallpaper, perfect lighting,(extremely detailed CG:1.2),"
    negative_prompt = "(NSFW:2), (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331), (morbid:1.21), (mutilated:1.21), (tranny:1.331), mutated hands, (poorly drawn hands:1.5), blurry, (bad anatomy:1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missing arms:1.331), (extra legs:1.331), (fused fingers:1.61051), (too many fingers:1.61051), (unclear eyes:1.331), lowers, bad hands, missing fingers, extra digit,bad hands, missing fingers, (((extra arms and legs))),NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331), (morbid:1.21), (mutilated:1.21), (tranny:1.331), mutated hands, (poorly drawn hands:1.5), blurry, (bad anatomy:1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missing arms:1.331), (extra legs:1.331), (fused fingers:1.61051), (too many fingers:1.61051), (unclear eyes:1.331), lowers, bad hands, missing fingers, extra digit,bad hands, missing fingers, (((extra arms and legs))),"

    def __init__(self):
        self.base_url = ""
        self.session = requests.Session()
        self.session.timeout = 30
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/83.0.4103.106 Safari/537.36"}

    @abc.abstractmethod
    def txt2img(self, txt: str, callback: Callable[[list[str]], None]) -> str:
        pass

    @abc.abstractmethod
    def get_models(self) -> str:
        pass

    @abc.abstractmethod
    def set_model(self, model_name: str) -> str:
        pass

    def _api_get(self, url_path: str, params: dict = None):
        url = self.base_url + url_path
        resp = self.session.get(url, params=params)
        return resp.json()

    def _api_post(self, url_path: str, data: dict = None):
        url = self.base_url + url_path
        resp = self.session.post(url, json=data)
        return resp.json()

    @staticmethod
    def trans2en(txt: str):
        chinese_pattern = re.compile(r'[\u4e00-\u9fff\uff00-\uffef]')  # Unicode范围：中文字符
        # if not match_chinese:
        #     prompt = "下面这段文字是否包含了任何不良的信息，如果包含了返回'1dog'，如果没有包含则返回原文(不要加任何前后缀): \n"
        #     return txt
        # else:
        #     prompt = "从现在开始你是一名基于输入描述的绘画AI提示词生成器，你会根据我输入的中文描述，生成符合主题的完整提示词。请注意，你生成后的内容服务于一个绘画AI，它只能理解具象的提示词而非抽象的概念，我将提供简短的描述，以便生成器可以为我提供准确的提示词。我希望生成的提示词能够包含人物的姿态、服装、妆容、情感表达和环境背景等细节，并且在必要时进行优化和重组以提供更加准确的描述，并且过滤掉不良的、不适合公共场所、NSFW的相关词汇，以便更好地服务于我的绘画AI，请严格遵守此条规则，也只输出翻译后的英文内容。请模仿结构示例生成准确提示词。示例输入：一位坐在床上的少女。 示例输出：1girl, sitting on, hand on own chest, head tilt, (indian_style:1.1), light smile, aqua eyes, (large breasts:1.2), blondehair, shirt, pleated_skirt, school uniform, (torn pantyhose:0.9), black garter belt, mary_janes, flower ribbon, glasses, looking at viewer, on bed,indoors,between legs. 请开始将下面的句子生成我需要的英文内容\n"
        prompt = "如果下面的内容或者翻译后的内容有不良的词汇就输出'1dog';(否则翻译成英文，不能翻译的词汇则保持原样.请直接输出翻译后的结果不要带任何附加信息):\n"
        result = chat("", prompt + txt)
        match_chinese = re.search(chinese_pattern, result)
        if match_chinese:
            return ""
        return result
