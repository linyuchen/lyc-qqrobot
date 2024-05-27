import asyncio
import threading

from nonebot import on_command, Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from nonebot.params import CommandArg

from src.common.game21.game21point import Game
from src.common.group_point import group_point_action


class Game21(Game):

    def __init__(self):
        super().__init__()
        self.currency = group_point_action.POINT_NAME

    def add_point(self, group_qq, qq, point):
        return group_point_action.add_point(group_qq, qq, point)

    def get_point(self, group_qq, qq):
        return group_point_action.get_member(group_qq, qq).point


group_instances = {}


def get_game_instance(group_qq: str):
    if group_qq in group_instances:
        return group_instances[group_qq]
    game = Game21()
    group_instances[group_qq] = game
    return game


game21_cmd = on_command("21点")


@game21_cmd.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    game = get_game_instance(str(event.group_id))
    try:
        point = int(args.extract_plain_text())
    except Exception as e:
        point = 100

    def reply(text):
        threading.Thread(target=lambda: asyncio.run(bot.send(event, text)), daemon=True).start()

    start_result = game.start_game(str(event.group_id), str(event.user_id), event.sender.card or event.sender.nickname,
                                   str(point), reply)

    start_result += "\n\n发送“21点换牌”可以换牌，换牌需要下注的十分之一费用\n"
    await game21_cmd.finish(start_result)


game21_update_cmd = on_command("21点换牌")


@game21_update_cmd.handle()
async def _(event: GroupMessageEvent):
    res = get_game_instance(str(event.group_id)).update_poker_list(str(event.group_id), str(event.user_id),
                                                                   event.sender.card or event.sender.nickname)
    await game21_update_cmd.finish(res)
