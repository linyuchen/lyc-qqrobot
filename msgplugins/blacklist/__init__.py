import json
from pathlib import Path

import config
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from ..cmdaz import CMD


class BlackListPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, )
    config_path = Path(__file__).parent / "config.json"
    config = []

    def __init__(self, qq_client=None):
        super().__init__(qq_client)
        self.read()

    def save(self):
        with open(self.config_path, "w") as f:
            f.write(json.dumps(self.config, indent=4, ensure_ascii=False))

    def read(self):
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                self.config = json.loads(f.read())

    def handle(self, msg: GroupMsg):
        qq = msg.group_member.qq
        if qq in self.config:
            msg.destroy()
            return
        if qq != str(config.ADMIN_QQ):
            return
        c = CMD("ignore", int_param_index=[0], param_len=1)
        no_c = CMD("noignore", int_param_index=[0], param_len=1)
        if c.az(msg.msg):
            black_qq = c.get_param_list()[0]
            self.config.append(black_qq)
            self.save()
            msg.reply(f"用户{c.get_param_list()[0]}已屏蔽")
            msg.destroy()
        elif no_c.az(msg.msg):
            black_qq = no_c.get_param_list()[0]
            self.config.remove(black_qq)
            self.save()
            msg.reply(f"用户{no_c.get_param_list()[0]}已取消屏蔽")
            msg.destroy()
