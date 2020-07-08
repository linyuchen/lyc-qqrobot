# coding=UTF8


class BaseMsg(object):
    """
    self.msg : string, 消息内容（过滤掉了表情和图片的）
    self.originalMsg : list, 原始的消息，没有过滤表情和图片
    self.time : int, 发送时间
    """
    msg: str = ""
    time: int = 0  # 发送时的时间戳
    is_over: bool = False  # 这条消息声明周期是否结束了，未结束就会传给下一个消息处理器
    paused: bool = False
    original_msg: list = []  # 这个已经没用了
    MSG_TYPE: str = ""

    def __init__(self):

        self.msg = ""
        self.time = 0

    def reply(self, content: str):
        """
        :param content:恢复内容
        :return:
        """

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

