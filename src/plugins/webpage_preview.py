import re
import time
from pathlib import Path
from typing import Callable, Coroutine

from nonebot import on_message, Bot
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, GroupMessageEvent
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="网页预览",
    description="GitHub、知乎、微信公众号文章、萌娘百科、百度搜索等网页预览",
    usage="发送链接即可"
)

import config
from src.common.browser.screenshot.weixin import screenshot_wx_article
from src.common.browser.screenshot.github import screenshot_github_readme
from src.common.browser.screenshot.zhihu import ZhihuPreviewer

zhihu_previewer = ZhihuPreviewer()

url_history = {}  # {"g群号": {"http://xxx": "最后一次获取时间戳"}}


def check_url_recent(qq: str, url: str) -> bool:
    now = time.time()
    if qq not in url_history:
        url_history[qq] = {}

    if url not in url_history[qq]:
        url_history[qq][url] = now
        return False
    if now - url_history[qq][url] > 5 * 60:
        url_history[qq][url] = now
        return False
    else:
        return True


async def screenshot(bot: Bot, event: MessageEvent, parse_url_func: Callable[[str], str | None],
                     screenshot_func: Callable[[str], Coroutine[str, None, Path]]):
    context_id = str(event.user_id) if not isinstance(event, GroupMessageEvent) else 'g' + str(event.group_id)
    msg_text = event.get_plaintext()
    url = parse_url_func(msg_text)
    if not url:
        return False
    if check_url_recent(context_id, url):
        return False
    img_path = await screenshot_func(url)
    if img_path:
        await bot.send(event, MessageSegment.image(img_path) + MessageSegment.text(url))
        img_path.unlink()
        return True
    return False


@on_message().handle()
async def zhihu_preview(bot: Bot, event: MessageEvent):
    def parse_zhihu_question_url(msg_text: str):
        if "//www.zhihu.com/question" in msg_text:
            """
            怎样搭配才能显得腿长？ - 知乎
            https://www.zhihu.com/question/27830729/answer/49839659
            https://www.zhihu.com/question/27830729
            """
            # 匹配知乎问题链接
            question_url = re.findall(r"https?://www.zhihu.com/question/\d+", msg_text)
            question_url = question_url[0] if question_url else None
            # 匹配知乎回答链接
            answer_url = re.findall(r"https?://www.zhihu.com/question/\d+/answer/\d+", msg_text)
            answer_url = answer_url[0] if answer_url else None
            url = answer_url or question_url
            return url

    await screenshot(bot, event, parse_zhihu_question_url, zhihu_previewer.screenshot_zhihu_question)

    def parse_zhihu_zhuanlan_url(msg_text):
        if "//zhuanlan.zhihu.com/p/" in msg_text:
            zhuanlan_url = re.findall(r"https://zhuanlan.zhihu.com/p/\d+", msg_text)
            zhuanlan_url = zhuanlan_url[0] if zhuanlan_url else None
            return zhuanlan_url

    await screenshot(bot, event, parse_zhihu_zhuanlan_url, zhihu_previewer.screenshot_zhihu_zhuanlan)


@on_message().handle()
async def github_preview(bot: Bot, event: MessageEvent):
    def parse_url(msg_text: str):
        if "//github.com/" in msg_text:
            # 获取github链接
            url = re.findall(r"https://github.com/[a-zA-Z0-9_/-]+", msg_text)
            url = url[0] if url else None
            return url

    await screenshot(bot, event, parse_url, lambda url: screenshot_github_readme(url, config.get_config('GFW_PROXY')))


@on_message().handle()
async def _(bot: Bot, event: MessageEvent):
    def parse_url(msg_text: str):
        if "mp.weixin.qq.com" in msg_text:
            # 获取github链接
            url = re.findall(r"https://mp.weixin.qq.com/s[/a-zA-Z0-9%?&=_-]+", msg_text)
            url = url[0] if url else None
            return url

    await screenshot(bot, event, parse_url, screenshot_wx_article)
