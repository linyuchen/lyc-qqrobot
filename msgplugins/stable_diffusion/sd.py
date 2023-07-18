import base64
import io
import uuid
from pathlib import Path

from PIL import Image

import config
from .base import AIDrawBase

base_url = config.SD_HTTP_API + "/sdapi/v1/"


class SDDraw(AIDrawBase):

    def __init__(self):
        super().__init__()
        self.base_url = base_url

    def txt2img(self, txt: str, width: int = 512, height: int = 512):
        """
        文字转图片
        :param txt: 文字
        :param width: 图片宽度
        :param height: 图片高度
        :return: 图片的base64编码
        """

        txt = txt.lower().replace("nsfw", "")
        if "I'm sorry" in txt:
            txt = ""
        txt = self.trans2en(txt)
        # 添加lora
        res_loras = self._api_get("loras")
        for lora in res_loras:
            txt += f",<lora:{lora['name']}:1>,"
        data = {
            "prompt": self.base_prompt + txt,
            "negative_prompt": self.negative_prompt,
            "steps": 20,
            "width": width,
            "height": height,
            "sampler_index": "DPM++ 2M Karras"
        }
        r = self._api_post("txt2img", data)
        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
            image_path = Path(__file__).parent / (str(uuid.uuid4()) + ".png")
            image.save(image_path)
            # image.show()
            return str(image_path)

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
        r = self._api_post("options", data)
        return f"模型已切换为：{model_name}"


if __name__ == '__main__':
    draw = SDDraw()
    # print(txt2img("1girl", 1024, 768))
    # print(txt2img("1girl,keqingdef,wake"))
    # print(txt2img("1girl, sky, sunshine, flowers,鸟在天上飞，阴部"))
    # print(txt2img("一个女孩在床上展示她的头发"))
    # print(txt2img("一个女孩在床上展示她的胸部"))
    print(draw.txt2img(
        "(watercolor pencil),1girl, nude,nipples,full body, spread leg, arm up, large breasts,shaved pussy,((heart-shaped pupils)),(uncensored) , sexually suggestive,saliva trail, suggestive fluid, (cum on body), tattoo, sweating, presenting, exhibitionism, wet cream dripping, female orgasm, liquid crystal fluid radiant cinematic lighting, solo uncensored cute assertive drunk blush"))
    # print(get_models())
    # text = "(masterpiece:1,2), best quality, masterpiece, highres, original, extremely detailed wallpaper, perfect lighting,(extremely detailed CG:1.2),"
    # pattern = re.compile(r'[\u4e00-\u9fff\uff00-\uffef]')  # Unicode范围：中文字符
    # match = res.search(pattern, text)
    # print(match)
    # print(get_models())
    # print(set_model("二次元：AbyssOrangeMix2_sfw"))
    # print(set_model("国风4"))
    # print(trans2en("裸体 女孩"))
