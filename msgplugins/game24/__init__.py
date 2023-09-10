# coding=UTF8

from ..msgcmd import cmdaz
from .import game24point
from ..superplugins import GroupPointAction
from qqsdk.message import MsgHandler, GroupMsg
CMD = cmdaz.CMD


class Game24Plugin(GroupPointAction, game24point.Game):
    
    def __init__(self):
        GroupPointAction.__init__(self)
        game24point.Game.__init__(self)
        self.currency = "活跃度"


class Game24(MsgHandler):
    __doc__ = """
    群游戏：21点
    """
    name = "24点"
    desc = "24点"
    bind_msg_types = (GroupMsg, )
    
    def __init__(self, **kwargs):

        super(Game24, self).__init__(**kwargs)
        self.cmdAnswer = CMD("答24点", param_len=1)
        self.cmdStart = CMD("24点")
        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样
        self.groupInstances = {}  # key groupQQ, value instance

    def get_game_instance(self, group_qq):
        return self.groupInstances.setdefault(group_qq, Game24Plugin())

    def handle(self, msg: GroupMsg):
        """
        此方法是用于处理事件接收到的消息
        注意此方法需存在一个参数用于传入消息实例
        """
        
        group_qq = msg.group.qq
        member = msg.group_member

        game = self.get_game_instance(group_qq)

        result = ""
        if self.cmdStart.az(msg.msg):
            result += game.start_game(msg.reply)
            result += "\n\n发送 “答24点 +空格+ 式子” 对24点游戏答题，加减乘除对应 + - * /,支持括号，如答24点 3*8*(2-1)\n"

        elif self.cmdAnswer.az(msg.msg):
            param = self.cmdAnswer.get_original_param()
            result += game.judge(group_qq, member.qq, member.get_name(), param)
 
        if result:
            msg.reply(result)
            msg.destroy()

