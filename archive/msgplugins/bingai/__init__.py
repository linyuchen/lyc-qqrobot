import requests

from common.cmd_alias import CMD_ALIAS_DRAW
from common.utils.nsfw_detector import nsfw_words_filter
from config import get_config
from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, FriendMsg, MessageSegment

bingai_host = get_config("BING_AI_API")


def bing(msg: GeneralMsg, params: list[str]):
    msg.reply("正在思考中……")
    if isinstance(msg, FriendMsg):
        user_id = msg.friend.qq + "f"
    else:
        user_id = msg.group.qq + "g"

    result = requests.post(bingai_host + "/chat", json={"user_id": user_id, "question": params[0]}).json()
    msg.reply(result["result"])


@on_command(
    cmd_name='#',
    ignores=("#include", "#define", "#pragma", "#ifdef", "#ifndef", "#ph"),
    desc="向机器人提问",
    example="#上海的天气",
    param_len=1,
    sep="",
    cmd_group_name="bingai",
    is_async=True
)
def bing_ai(msg: GeneralMsg, params: list[str]):
    bing(msg, params)


@on_command("bing",
            desc="向bing ai提问",
            example="bing 上海的天气",
            param_len=1,
            sep=" ",
            cmd_group_name="bingai",
            is_async=True
            )
def bing_ai2(msg: GeneralMsg, params: list[str]):
    bing(msg, params)


@on_command(
    "DE3",
    alias=("bing画图", "de3", "微软画图") + CMD_ALIAS_DRAW,
    priority=5,
    param_len=1,
    desc="DALL·E 3画图",
    example="de3 一只猫",
    cmd_group_name="bingai",
    is_async=True
)
def bingai_draw(msg: GeneralMsg, params: list[str]):
    prompt = params[0]
    prompt = nsfw_words_filter(prompt)
    if not prompt:
        msg.reply("提示词中含有敏感词汇，请重新输入")
        return
    msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")
    result = requests.post(bingai_host + "/draw", json={"prompt": prompt}).json()
    preview = result["result"]["preview"]
    img_urls = result["result"]["urls"]
    err = result.get('err')
    if err:
        return msg.reply(err)
    # msg.reply(result["result"])
    msg.reply(
        MessageSegment.image_b64(preview) +
        MessageSegment.text(f"提示词:{prompt}\n\n原图：\n" +
                            "\n".join([f"{index + 1}. {url}" for index, url in enumerate(img_urls)]))
    )
