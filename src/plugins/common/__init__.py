from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, Bot, MessageEvent


def is_at_me(event: GroupMessageEvent) -> bool:
    for segment in event.original_message:
        if segment.type == "at" and segment.data.get("qq") == str(event.self_id):
            return True


def get_message_image_urls(message: Message):

    image_msg_segments = message.get('image')
    image_urls = [image.data['url'] for image in image_msg_segments]
    mface_msg_segments = message.get('mface')
    mface_urls = [image.data['url'] for image in mface_msg_segments]
    return image_urls + mface_urls
