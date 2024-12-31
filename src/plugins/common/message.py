from nonebot.adapters.onebot.v11 import Message
from nonebot_plugin_alconna import UniMsg, Image


def get_message_image_urls(message: UniMsg):
    image_msg_segments = message.get(Image)
    image_urls = [image.url for image in image_msg_segments]
    # mface_msg_segments = message.get('mface')
    # mface_urls = [image.data['url'] for image in mface_msg_segments]
    return image_urls # + mface_urls
