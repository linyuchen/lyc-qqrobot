from typing import Optional, List, Literal

from pydantic import BaseModel, AnyUrl, HttpUrl, Field, ConfigDict, Json


class ConfigAIChat(BaseModel):
    api_key: str
    base_url: Optional[str] = None
    model: str

class Config(BaseModel):
    ai_chats: List[ConfigAIChat] = Field(default_factory=list)
    http_proxy: Optional[HttpUrl] | Literal[''] = Field(default='')


CONFIG: Config = Config()

def set_config(config: Config):
    global CONFIG
    CONFIG = config
