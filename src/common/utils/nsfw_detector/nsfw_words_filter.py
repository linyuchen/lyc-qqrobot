import json
import re
from pathlib import Path

BANNED_WORDS = json.load(open(Path(__file__).parent / "banned_words.json"))
BANNED_WORDS = [word["words"].strip().lower() for word in BANNED_WORDS]


def nsfw_words_filter(text: str) -> str:
    # 特殊符号转成空格
    text = re.sub(r'[,，。.(){}:]+', ' ', text)
    result = []
    for prompt_word in text.split():
        if prompt_word in BANNED_WORDS:
            # have_banned_words.append(prompt_word)
            continue
        result.append(prompt_word)
    return " ".join(result)
