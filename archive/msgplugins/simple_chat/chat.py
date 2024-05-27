import random
import time
from pathlib import Path
from typing import TypedDict

data_path = Path(__file__).parent / "data.txt"


class Data(TypedDict):
    tags: list[str]
    words: list[str]


context = {}  # {context_id: str, tags: list[str], trigger_time: time.time()}


def __get_data():
    data: list[Data] = []
    with open(data_path, "r", encoding="utf-8") as f:
        text = f.readline()
        text = text.split("|")
        tag_txt = text[0]
        tags = tag_txt.split(",")
        map(lambda x: x.strip(), tags)
        words = text[1:]
        data.append({"tags": tags, "words": words})

    return data


def get_word(context_id: str, msg: str):
    data = __get_data()
    for d in data:
        tags = d["tags"]
        words = d["words"]
        for tag in tags:
            if tag in msg:
                current_context = context.setdefault(context_id, {"tags": tags, "trigger_time": 0.0})
                if time.time() - current_context["trigger_time"] > 60 * 60:
                    current_context["trigger_time"] = time.time()
                    r = random.randint(0, 10)
                    if r < 3:  # 百分之三十的概率触发
                        return random.choice(words)
    return None


if __name__ == '__main__':
    # __get_data()
    print(get_word("123", "op"))
    print(get_word("123", "原神"))