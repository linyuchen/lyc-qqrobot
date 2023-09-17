import base64
import io
import tempfile
from pathlib import Path

import aiohttp
import requests
from PIL import Image

import config
from common.sdwebuiapi import WebUIApi, raw_b64_img
from common.utils.translator import trans, is_chinese
from .base import AIDrawBase

base_url = config.SD_HTTP_API + "/sdapi/v1/"


class SDDraw(AIDrawBase):

    def __init__(self):
        super().__init__()
        self.base_url = base_url
        self.host = self.base_url.split(":")[1].split("/")[2]
        self.port = self.base_url.split(":")[2].split("/")[0]
        self.webui_api = WebUIApi(host=self.host, port=self.port)

    def trans_prompt(self, txt):
        txt = txt.lower().replace("nsfw", "")
        if is_chinese(txt):
            txt = trans(txt)
        return txt

    def txt2img(self, txt: str, width: int = 1024, height: int = 1024) -> list[Path]:
        """
        文字转图片
        :param txt: 文字
        :param width: 图片宽度
        :param height: 图片高度
        :return: 图片路径列表
        """

        txt = self.trans_prompt(txt)
        # if "I'm sorry" in txt:
        #     txt = ""
        # 添加lora
        # res_loras = self._api_get("loras")
        # for lora in res_loras:
        #     txt += f",<lora:{lora['name']}:1>,"
        data = {
            "prompt": self.base_prompt + txt,
            "negative_prompt": self.negative_prompt,
            "steps": 20,
            "width": width,
            "height": height,
            "sampler_index": "DPM++ 2M Karras",
        }
        r = self._api_post("txt2img", data)
        res_paths = []
        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
            image_path = tempfile.mktemp(suffix=".png")
            image.save(image_path)
            res_paths.append(Path(image_path))
        return res_paths

    def img2img(self, img_url: str, prompt: str) -> str:
        prompt = self.trans_prompt(prompt)
        data = requests.get(img_url).content
        fp = io.BytesIO(data)
        image = Image.open(fp)
        size = image.size
        # if size[0] > 768 or size[1] > 768:
        max_size = 768
        size = (max_size, int(size[1] / size[0] * max_size))
        resp = self.webui_api.img2img([image],
                                      prompt=self.base_prompt + prompt,
                                      negative_prompt=self.negative_prompt,
                                      width=size[0],
                                      height=size[1],
                                      denoising_strength=0.5
                                      )
        image = resp.images[0]
        return image
        #
        # return raw_b64_img(image)

    def __get_models(self):
        res = self._api_get("sd-models")
        options = self._api_get("options")
        current_model_hash = options["sd_checkpoint_hash"]
        models = []
        for m in res:
            model_name = m["model_name"]
            if current_model_hash == m["sha256"]:
                model_name = f"*当前模型：{model_name}*"
            models.append(model_name)
        models = "\n".join(models)
        return models

    def __get_loras(self):
        res = self._api_get("loras")
        # loras = [{"name": lora["name"], "frequency_tag": lora["metadata"]["ss_tag_frequency"].keys()} for lora in res]
        loras = []
        for lora in res:
            trigger_tags = lora["metadata"].get("ss_tag_frequency", {}).keys()
            if not trigger_tags:
                continue
            trigger_tags = [tag.split("_")[1] for tag in trigger_tags]
            trigger_tags = "，".join(trigger_tags)
            loras.append(f"{lora['name']}：{trigger_tags}")

        loras = "\n\n".join(loras)
        return loras

    def get_models(self):
        res = f"模型列表：\n{self.__get_models()}"
        return res

    def get_loras(self):
        res = f"lora列表：\n{self.__get_loras()}"
        return res

    def set_model(self, model_name: str):
        res = self._api_get("sd-models")
        model = filter(lambda m: model_name in m["model_name"], res)
        model = list(model)
        if len(model) == 0:
            return f"模型{model_name}不存在"
        model_name = model[0]["model_name"]
        data = {
            "sd_model_checkpoint": model_name
        }
        self._api_post("options", data)
        return f"模型已切换为：{model_name}"
