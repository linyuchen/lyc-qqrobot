# -*- encoding:UTF8 -*-
from dataclasses import dataclass

from qqsdk.message.basemsg import BaseMsg


@dataclass
class ErrorMsg(BaseMsg):
    pass
