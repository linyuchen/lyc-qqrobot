# coding=UTF8

"""
可视化菜单
当前目录下的所有txt(utf8编码)都是菜单
txt文件名即菜单绑定的命令
"""
import os
from qqsdk.message import MsgHandler, FriendMsg, GroupMsg, BaseMsg
from .visualmenu import VisualMenu
curPath = os.path.dirname(__file__)


class MenuEvent(MsgHandler, VisualMenu):
    bind_msg_types = (FriendMsg, GroupMsg)

    def __init__(self, qq_client):

        super(MenuEvent, self).__init__(qq_client)
        VisualMenu.__init__(self)

    def handle(self, msg: BaseMsg):

        msg_content = msg.msg.strip()
        menu = self.allMenu.copy()
        if isinstance(msg, GroupMsg):
            menu.update(self.groupMenu.items())
        elif isinstance(msg, FriendMsg):
            pass
            # if msg.friend.qq in robot_config.admins:
            #     menu.update(self.adminMenu.items())

        for i in self.cmdNameList:

            if msg_content == i:
                result: str = menu.get(i, None)
                if result:
                    msg.reply(result)
                    msg.destroy()
                break

