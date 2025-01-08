from typing import Optional, List, Literal

from pydantic import BaseModel, AnyUrl, HttpUrl, Field, ConfigDict


class ConfigAIChat(BaseModel):
    api_key: str
    base_url: str
    model: str

class Config(BaseModel):
    ai_chats: List[ConfigAIChat]
    http_proxy: Optional[HttpUrl] | Literal[''] = Field(default='')


CONFIG: Config = Config(ai_chats=[])

def set_config(config: Config):
    global CONFIG
    CONFIG = config
