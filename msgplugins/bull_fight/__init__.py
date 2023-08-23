# coding=UTF8
import threading

from msgplugins.bull_fight import bullfight
from msgplugins.msgcmd.cmdaz import CMD
from msgplugins.superplugins import GroupPointAction
from qqsdk.message import MsgHandler, GroupMsg


class BullGame(GroupPointAction, bullfight.BullFight):

    def __init__(self, group_qq, qq_client):
        bullfight.BullFight.__init__(self, group_qq, qq_client)
        GroupPointAction.__init__(self)


# 新建个事件类，继承于MsgEvent
class BullFightPlugin(MsgHandler):
    __doc__ = u"""
    群游戏：斗牛
    """
    name = "斗牛"
    desc = "发送 斗牛 + 数字 开始斗牛游戏，数字为下注金额\n下注金额0可坐庄"
    bind_msg_types = (GroupMsg,)

    def __init__(self, **kwargs):
        super(BullFightPlugin, self).__init__(**kwargs)
        self.group_instances = {}  # key groupQQ, value instance

        # 不同的QQ群用不同的实例， 因为一个人可以在多个群里

    def get_game_instance(self, group_qq):

        group_plugin = BullGame(group_qq, self.qq_client)
        return self.group_instances.setdefault(group_qq, group_plugin)

    def handle(self, msg: GroupMsg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        group_qq = msg.group.qq
        member = msg.group_member

        __game = self.get_game_instance(group_qq)
        cmd_start = CMD("斗牛", param_len=1, sep="")
        if cmd_start.az(msg.msg):
            msg.destroy()
            param = cmd_start.get_param_list()[0]

            def func():
                result = __game.start_game(member.qq, member.get_name(), msg.reply, param)

                if result:
                    msg.reply(result)

            threading.Thread(target=func).start()
