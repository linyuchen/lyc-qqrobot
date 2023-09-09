import asyncio
import re
import threading
import time
from collections import OrderedDict

import config
from common.logger import logger
from common.utils.postimg import postimg_cc
from msgplugins.msgcmd.cmdaz import on_command
from qqsdk.message import GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .midjourney_client import TaskCallbackResponse, TaskCallback, TaskType
from .midjourney_websocket_client import MidjourneyClient

mj_client = MidjourneyClient(token=config.MJ_DISCORD_TOKEN,
                             channel_id=config.MJ_DISCORD_CHANNEL_ID,
                             guild_id=config.MJ_DISCORD_GUILD_ID,
                             proxy=config.GFW_PROXY)

CMD_GROUP_NAME = "MJ画图"


class LastDrawRes:
    def __init__(self, res: TaskCallbackResponse):
        self.res = res
        self.already_upscale_index = []


last_task_res = {}  # key: userid, value: LastDrawRes
msg_task_res = OrderedDict()  # key: img_url, value: LastDrawRes


def get_user_id(msg: GroupMsg | FriendMsg):
    if isinstance(msg, GroupMsg):
        user_id = f"g{msg.group.qq}"
    else:
        user_id = f"q{msg.friend.qq}"
    return user_id


@on_command("画图", alias=("mj", "niji", "画画", "绘图", "画一", "画个", "给我画", "帮我画", "画张"),
            param_len=-1,
            desc="@机器人后发送 画图+空格+描述 进行AI画图,如 画图 一只猫在天上飞",
            cmd_group_name=CMD_GROUP_NAME)
def mj_draw(msg: GroupMsg | FriendMsg, msg_param: str):
    if isinstance(msg, GroupMsg):
        if not msg.is_at_me:
            return

    def callback(res: TaskCallbackResponse):
        if res.error:
            msg.reply(res.error)
        elif res.image_path:
            img_url = res.image_urls[0]
            img_url = asyncio.run(postimg_cc(img_url))
            reply_msg = MessageSegment.image_path(res.image_path[0])
            reply_msg += MessageSegment.text(f"提示词:{res.task.prompt}\n\n原图(复制到浏览器打开):{img_url}\n\n")
            if res.task.task_type == TaskType.DRAW:
                last_draw_res = LastDrawRes(res)
                last_task_res[get_user_id(msg)] = last_draw_res
                msg_task_res[img_url] = last_draw_res
                if len(msg_task_res) > 100:
                    msg_task_res.pop(list(msg_task_res.keys())[0])
                reply_msg += MessageSegment.text("回复u+数字取图,如u1\n上面两张为1、2，下面为3、4")
                msg.reply(reply_msg)
            elif res.task.task_type == TaskType.UPSCALE:
                msg.reply(reply_msg, at=False)
            res.image_path[0].unlink(missing_ok=True)

    msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")
    # 获取图片
    img_urls = []
    if msg.quote_msg:
        urls = msg.quote_msg.msg_chain.get_image_urls()
        img_urls.extend(urls)
    msg_chain = msg.msg_chain
    if msg_chain:
        urls = msg_chain.get_image_urls()
        img_urls.extend(urls)
    # 批量上传到图床,这里要用异步
    img_post_urls = []

    async def post_img():
        async def task(__url):
            try:
                logger.debug(f"上传图片{__url}到图床")
                start_time = time.time()
                res_url = await postimg_cc(__url, resp_short=False)
                end_time = time.time()
                used_time = end_time - start_time
                logger.debug(f"上传图片{__url}到图床成功,耗时{int(used_time)}秒")
            except Exception as e:
                logger.error(f"上传图片到图床失败:{e}")
                return
            img_post_urls.append(res_url)

        tasks = []
        for url in img_urls:
            tasks.append(asyncio.create_task(task(url)))
        await asyncio.gather(*tasks)

    def reply_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(post_img())
        if not msg_param and img_post_urls:
            prompt = "8k "
        else:
            prompt = " ".join(msg_param)
        if msg.msg.startswith("niji"):
            prompt += " --niji 5"
            if "--style" not in prompt:
                prompt += " --style original"
        if not prompt:
            return msg.reply("请输入提示词或者附上图片")
        mj_client.draw(prompt, callback, img_post_urls)

    threading.Thread(target=reply_thread, daemon=True).start()


@on_command("取图", alias=("U", "u"), param_len=1, int_param_index=[0], sep="", cmd_group_name=CMD_GROUP_NAME)
def mj_upscale(msg: GroupMsg | FriendMsg, msg_param: list[str]):
    last_res: LastDrawRes = last_task_res.get(get_user_id(msg))
    if msg.quote_msg and msg.quote_msg.msg_chain.get_image_urls():
        img_url = re.findall(r"(http\S+)", msg.quote_msg.msg)
        if img_url:
            img_url = img_url[0]
            _ = msg_task_res.get(img_url)
            if _:
                last_res = _

    if not msg_param[0].isnumeric():
        return
    upscale_index = int(msg_param[0])
    if not last_res:
        msg.reply("你还没有画图哦")
        return
    if upscale_index in last_res.already_upscale_index:
        msg.reply(f"已经取过图{upscale_index}啦")
        return
    if upscale_index < 1 or upscale_index > 4:
        msg.reply("取图序号必须在1-4之间")
        return
    last_res.already_upscale_index.append(upscale_index)
    msg.reply("正在取图中，请稍等...")
    mj_client.upscale(last_res.res, upscale_index)
