import asyncio
import threading

from nonebot import on_command, Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from nonebot.params import CommandArg

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="斗牛",
    description="斗牛棋牌游戏",
    usage="斗牛 下注数量，如斗牛 100",
)

from src.common.bullfight import BullFight
from src.common.group_point import group_point_action
from src.plugins._common.rules import rule_args_num



class BullGame(BullFight):

    def __init__(self, group_qq):
        BullFight.__init__(self, group_qq)

    def add_point(self, group_qq, qq, point) -> int:
        return group_point_action.add_point(group_qq, qq, point)

    def get_point(self, group_qq, qq) -> int:
        return group_point_action.get_member(group_qq, qq).point


group_instances: dict[str, BullGame] = {}


def get_game_instance(group_qq):
    if group_qq not in group_instances:
        game = BullGame(group_qq)
        group_instances[group_qq] = game
    else:
        game = group_instances[group_qq]
    return game


bull_game_cmd = on_command('斗牛', force_whitespace=True, rule=rule_args_num(1))


@bull_game_cmd.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    game = get_game_instance(str(event.group_id))

    def reply(text):
        threading.Thread(target=lambda: asyncio.run(bot.send(event, text))).start()

    def start():
        start_result = game.start_game(str(event.user_id), str(event.sender.card or event.sender.nickname),
                                       reply,
                                       args.extract_plain_text().strip())
        asyncio.run(bot.send(event, start_result))

    threading.Thread(target=start, daemon=True).start()
    await bull_game_cmd.finish()
