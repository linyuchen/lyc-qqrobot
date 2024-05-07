import abc
from typing import Callable

import requests


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
