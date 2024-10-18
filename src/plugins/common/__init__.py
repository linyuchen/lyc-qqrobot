from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Message


def get_message_image_urls(message: Message):

    image_msg_segments = message.get('image')
    image_urls = [image.data['url'] for image in image_msg_segments]
    mface_msg_segments = message.get('mface')
    mface_urls = [image.data['url'] for image in mface_msg_segments]
    return image_urls + mface_urls


def check_super_user(user_id: str):
    return user_id in get_driver().config.superusers