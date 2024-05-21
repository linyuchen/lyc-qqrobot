from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Message
from nonebot.params import CommandArg

from src.common.group_point import group_point_action

sign_cmd = on_command('签到')


@sign_cmd.handle()
async def _(event: GroupMessageEvent):
    sign_result = group_point_action.sign(str(event.group_id), str(event.user_id),
                                          event.sender.card or event.sender.nickname)
    await sign_cmd.finish(MessageSegment.reply(event.message_id) + sign_result)


my_group_point_cmd = on_command('活跃度', aliases={'我的活跃度', '查询活跃度'})


@my_group_point_cmd.handle()
async def _(event: GroupMessageEvent):
    point_result = group_point_action.get_point(str(event.group_id), str(event.user_id))
    await my_group_point_cmd.finish(MessageSegment.reply(event.message_id) + point_result)


point_rank_cmd = on_command('活跃度排名', aliases={'活跃度排行榜', '活跃度排名榜'})


@point_rank_cmd.handle()
async def _(event: GroupMessageEvent):
    rank_result = group_point_action.get_point_rank(str(event.group_id))
    await point_rank_cmd.finish(MessageSegment.reply(event.message_id) + rank_result)


transfer_point_cmd = on_command('转活跃度', aliases={'转账活跃度', '活跃度转账', '转账'})


@transfer_point_cmd.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    at_messages = event.message.get('at', 1)
    if not at_messages:
        return
    at_message = at_messages[0]
    other_user_id = at_message.data.get('qq')
    try:
        point = int(args.extract_plain_text().strip())
    except Exception as e:
        return
    transfer_result = group_point_action.transfer_point(str(event.group_id), str(event.user_id), str(other_user_id),
                                                        point)
    await transfer_point_cmd.finish(MessageSegment.reply(event.message_id) + transfer_result)
