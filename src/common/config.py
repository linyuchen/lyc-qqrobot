from typing import Optional, List, Literal

from pydantic import BaseModel, AnyUrl, HttpUrl, Field, ConfigDict


class ConfigChatGPT(BaseModel):
    key: str
    api: AnyUrl
    model: str

class Config(BaseModel):
    chatgpt: List[ConfigChatGPT]
    http_proxy: Optional[HttpUrl] | Literal[''] = Field(default='')


CONFIG: Config = Config(chatgpt=[])

def set_config(config: Config):
    global CONFIG
    CONFIG = config
