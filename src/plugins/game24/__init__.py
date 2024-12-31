import asyncio
import threading

from nonebot import on_command, Bot, on_fullmatch
from nonebot.params import CommandArg, Message, Event
from nonebot.plugin import PluginMetadata
from nonebot_plugin_uninfo import Uninfo

__plugin_meta__ = PluginMetadata(
    name="24点",
    description="24点口算游戏",
    usage="24点"
)

from src.common.game24 import game24point
from src.common.group_point import group_point_action
from src.plugins.common.rules import rule_args_num


class Game24(game24point.Game):

    def __init__(self):
        super().__init__()
        self.currency = group_point_action.POINT_NAME

    def add_point(self, group_qq: str, member_qq: str, point: int):
        group_point_action.add_point(group_qq, member_qq, point)

    def get_point(self, group_qq: str, member_qq: str) -> int:
        return group_point_action.get_member(group_qq, member_qq).point


game_instances: dict[str, Game24] = {}


def get_game_instance(group_qq: str):
    if group_qq in game_instances:
        return game_instances[group_qq]

    game = Game24()
    game_instances[group_qq] = game
    return game


start_game24_cmd = on_fullmatch('24点')


@start_game24_cmd.handle()
async def _(bot: Bot, event: Event, session: Uninfo):
    if not session.scene.is_group:
        return
    group_id = session.group.id
    game = get_game_instance(str(group_id))

    def reply(text: str):
        threading.Thread(target=lambda: asyncio.run(bot.send(event, text)), daemon=True).start()

    start_result = game.start_game(reply)
    start_result += "\n\n发送 “答24点 +空格+ 式子” 对24点游戏答题，加减乘除对应 + - * /,支持括号，如答24点 3*8*(2-1)\n"
    await start_game24_cmd.finish(start_result)


answer_game24_cmd = on_command('答24点', rule=rule_args_num(num=1))


@answer_game24_cmd.handle()
async def _(event: Event, session: Uninfo, args: Message = CommandArg()):
    if not session.scene.is_group:
        return
    group_id = session.group.id
    user_id = session.user.id
    user_nick = session.user.nick
    game = get_game_instance(str(group_id))
    res = game.judge(str(group_id), str(user_id), user_nick, args.extract_plain_text())
    await answer_game24_cmd.finish(res)
