# coding=UTF8

from msgplugins.cmdaz import CMD
from qqsdk.message import MsgHandler, GroupMsg
from msgplugins.bull_fight import bullfight
from msgplugins.superplugins import GroupPointAction


class BullGame(GroupPointAction, bullfight.BullFight):

    def __init__(self, group_qq, qq_client):
        bullfight.BullFight.__init__(self, group_qq, qq_client)
        GroupPointAction.__init__(self)


# 新建个事件类，继承于MsgEvent
class MyEvent(MsgHandler):
    __doc__ = u"""
    群游戏：斗牛
    """
    bind_msg_types = (GroupMsg, )
    
    def __init__(self, qq_client):
        super(MyEvent, self).__init__(qq_client)
        self.name = "group_gamble"
        self.cmdStart = CMD("斗牛", param_len=1)
        self.groupInstances = {}  # key groupQQ, value instance

        # 不同的QQ群用不同的实例， 因为一个人可以在多个群里

    def get_game_instance(self, group_qq):

        group_plugin = BullGame(group_qq, self.qq_client)
        return self.groupInstances.setdefault(group_qq, group_plugin)

    def handle(self, msg: GroupMsg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        group_qq = msg.group.qq
        member = msg.group_member

        __game = self.get_game_instance(group_qq)

        result = ""
        if self.cmdStart.az(msg.msg):
            param = self.cmdStart.get_param_list()[0]
            result += __game.start_game(member.qq, member.get_name(), msg.reply, param)

        if result:
            msg.reply(result)
            msg.destroy()

