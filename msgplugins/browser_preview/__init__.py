import re

import config
from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, MessageSegment
from .browser_screenshot import search_baidu, ZhihuPreviewer, github_readme

zhihu_previewer = ZhihuPreviewer()

@on_command("百度",
            param_len=1,
            desc="百度 搜索内容",
            cmd_group_name="百度"
            )
def baidu(msg: GeneralMsg, params: list[str]):
    """
    百度搜索
    """
    img_path = search_baidu(params[0])
    msg.reply(MessageSegment.image_path(img_path))
    img_path.unlink()


@on_command("", cmd_group_name="知乎预览")
def zhihu_preview(msg: GeneralMsg, params: list[str]):
    if "//www.zhihu.com/question" in msg.msg:

        """
        怎样搭配才能显得腿长？ - 知乎
        https://www.zhihu.com/question/27830729/answer/49839659
        https://www.zhihu.com/question/27830729
        """
        # 匹配知乎问题链接
        question_url = re.findall(r"https://www.zhihu.com/question/\d+", msg.msg)
        question_url = question_url[0] if question_url else None
        # 匹配知乎回答链接
        answer_url = re.findall(r"https://www.zhihu.com/question/\d+/answer/\d+", msg.msg)
        answer_url = answer_url[0] if answer_url else None
        url = answer_url or question_url
        if url:
            msg.destroy()
            img_path = zhihu_previewer.zhihu_question(url)
            if img_path:
                msg.reply(MessageSegment.image_path(img_path) + MessageSegment.text(url), at=False)
                img_path.unlink()
                return

    elif "//zhuanlan.zhihu.com/p/" in msg.msg:
        zhuanlan_url = re.findall(r"https://zhuanlan.zhihu.com/p/\d+", msg.msg)
        zhuanlan_url = zhuanlan_url[0] if zhuanlan_url else None
        if zhuanlan_url:
            msg.destroy()
            img_path = zhihu_previewer.zhihu_zhuanlan(zhuanlan_url)
            if img_path:
                msg.reply(MessageSegment.image_path(img_path) + MessageSegment.text(zhuanlan_url), at=False)
                img_path.unlink()
                return


@on_command("", cmd_group_name="github预览")
def github_preview(msg: GeneralMsg, params: list[str]):
    if "//github.com/" in msg.msg:
        # 获取github链接
        url = re.findall(r"https://github.com/[\w_/-]+", msg.msg)
        url = url[0] if url else None
        if url:
            msg.destroy()
            img_path = github_readme(url, http_proxy=config.get_config("GFW_PROXY"))
            if img_path:
                msg.reply(MessageSegment.image_path(img_path) + MessageSegment.text(url), at=False)
                img_path.unlink()
                return


@on_command("萌娘百科", param_len=1, desc="萌娘百科搜索,如:萌娘百科 猫娘")
def moe_wiki(msg: GeneralMsg, params: list[str]):
    msg.reply("正在为您搜索萌娘百科...")
    img_path = moe_wiki(params[0])
    if img_path:
        msg.reply(MessageSegment.image_path(img_path))
        img_path.unlink()

