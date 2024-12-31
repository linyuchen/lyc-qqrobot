from nonebot import on_command, on_fullmatch
from nonebot.params import CommandArg, Message
from nonebot.plugin import PluginMetadata
from nonebot_plugin_uninfo import Uninfo
from nonebot_plugin_alconna import UniMsg, At

__plugin_meta__ = PluginMetadata(
    name="群积分",
    description="群积分系统",
    usage="签到、活跃度、活跃度排名、转活跃度 @对方 活跃度数量",
)

from src.common.group_point import group_point_action
from src.plugins.common.rules import rule_is_group_msg

sign_cmd = on_fullmatch('签到', rule=rule_is_group_msg())


@sign_cmd.handle()
async def _(session: Uninfo, msg: UniMsg):
    group_id = session.group.id
    user_id = session.user.id
    user_nick = session.user.nick
    sign_result = group_point_action.sign(str(group_id), str(user_id), user_nick)
    await sign_cmd.finish(await (UniMsg.reply(msg.get_message_id()) + sign_result).export())


my_group_point_cmd = on_fullmatch(('活跃度', '我的活跃度', '查询活跃度'), rule=rule_is_group_msg())


@my_group_point_cmd.handle()
async def _(session: Uninfo, msg: UniMsg):
    group_id = session.group.id
    user_id = session.user.id
    point_result = group_point_action.get_point_info(str(group_id), str(user_id))
    await my_group_point_cmd.finish(await (UniMsg.reply(msg.get_message_id()) + point_result).export())


point_rank_cmd = on_fullmatch(('活跃度排名', '活跃度排行榜', '活跃度排名榜'), rule=rule_is_group_msg())


@point_rank_cmd.handle()
async def _(session: Uninfo, msg: UniMsg):
    rank_result = group_point_action.get_point_rank(str(session.group.id))
    await point_rank_cmd.finish(await (UniMsg.reply(msg.get_message_id()) + rank_result).export())


transfer_point_cmd = on_command('转活跃度', aliases={'转账活跃度', '活跃度转账', '转账'}, rule=rule_is_group_msg())


@transfer_point_cmd.handle()
async def _(session: Uninfo, msg: UniMsg, args: Message = CommandArg()):
    group_id = session.group.id
    user_id = session.user.id
    at_messages = msg.get(At, 1)
    if not at_messages:
        return
    at_message: At = at_messages[0]
    other_user_id = at_message.target
    point = args.extract_plain_text().strip()
    if not point.isdigit():
        return
    transfer_result = group_point_action.transfer_point(str(group_id), str(user_id), str(other_user_id), point)
    await transfer_point_cmd.finish(await (UniMsg.reply(msg.get_message_id()) + transfer_result).export())
