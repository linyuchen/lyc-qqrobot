# coding=UTF8
from dataclasses import dataclass
from .segment import MessageSegment


@dataclass
class BaseMsg:
    """
    self.msg : string, 消息内容（过滤掉了表情和图片的）
    self.originalMsg : list, 原始的消息，没有过滤表情和图片
    self.time : int, 发送时间
    """
    msg: str = ""
    time: int = 0  # 发送时的时间戳
    is_over: bool = False  # 这条消息声明周期是否结束了，未结束就会传给下一个消息处理器
    paused: bool = False
    MSG_TYPE: str = ""

    def reply(self, content: str | MessageSegment):
        """
        :param content:回复内容
        :return:
        """
        raise NotImplementedError

    def pause(self):
        """
        暂停向下一个event传播
        """

        self.paused = True

    def resume(self):
        """
        与pause相反，恢复向下一个event传播
        """

        self.paused = False

    def destroy(self):
        """
        销毁此消息，不再让其他event处理
        """
        self.is_over = True
