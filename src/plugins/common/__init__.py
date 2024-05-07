from nonebot.adapters.onebot.v11 import GroupMessageEvent


def is_at_me(event: GroupMessageEvent) -> bool:
    for segment in event.original_message:
        if segment.type == "at" and segment.data.get("qq") == str(event.self_id):
            return True
