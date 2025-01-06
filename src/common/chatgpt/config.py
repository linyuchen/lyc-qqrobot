from typing import Optional, List

from pydantic import BaseModel, AnyUrl, HttpUrl, Field, ConfigDict


class ConfigItem(BaseModel):
    key: str
    api: AnyUrl
    model: str




class ChatGPTConfig(BaseModel):
    chatgpt: List[ConfigItem]
    gfw_proxy: Optional[HttpUrl] | str = Field(default='')


CHATGPT_CONFIG = ChatGPTConfig

def set_chatgpt_config(config: ChatGPTConfig):
    global CHATGPT_CONFIG
    CHATGPT_CONFIG = config
