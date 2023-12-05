# lora的翻译和绑定, 存放在本文件目录下的lora.json中
"""
lora文件名:{  # 这里的文件名不需要后缀
    触发词中文翻译: 触发词英文原词
}

example:
    有个lora文件叫星穹铁道-符玄.safetensors，它的触发词是fuxuan
    {
        "星穹铁道-符玄": {
            "符玄": "fuxuan",
        }
    }
    用户的提示词中有符玄，就会被替换成 <lora: 星穹铁道-符玄>,fuxuan
"""
import json
from pathlib import Path

lora_path = Path(__file__).parent / "lora.json"


def get_lora() -> dict:
    if not lora_path.exists():
        return {}
    with open(lora_path, "r", encoding="utf8") as f:
        lora = json.load(f)
        return lora


def get_lora_format() -> str:
    lora = get_lora()
    result = ""
    for lora_name in lora:
        result += f"{lora_name}:\n" + "，".join(lora[lora_name].keys()) + "\n\n"

    return result


def trans_lora(prompt: str) -> tuple[str, str]:
    lora = get_lora()
    lora_prompts = []
    new_prompts = []
    old_prompts = []
    for prompt in prompt.split(","):
        new_prompt = ""
        for key in lora:
            lora_keys = list(lora[key].keys())
            lora_keys.sort(key=len, reverse=True)
            for lora_key in lora_keys:
                lora_word = lora[key][lora_key]
                if lora_key in prompt:
                    if lora_word not in lora_prompts:
                        lora_prompts.append(f"<lora:{key}>")
                    new_prompt = prompt.replace(lora_key, lora_word + ",")
                    prompt = prompt.replace(lora_key, "")

        if new_prompt:
            new_prompts.append(new_prompt)

        old_prompts.append(prompt)

    return ",".join(lora_prompts) + "," + ",".join(new_prompts), ",".join(old_prompts)


if __name__ == '__main__':
    print(trans_lora("刻晴泳装,水里"))
