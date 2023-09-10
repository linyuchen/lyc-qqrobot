from msgplugins.msgcmd.cmdaz import on_command
from qqsdk.message import GroupMsg, FriendMsg, MessageSegment
from .genshinvoice_top import tts, speakers


@on_command("tts列表", param_len=0,
            desc="tts列表",
            cmd_group_name="tts")
def tts_list(msg: GroupMsg | FriendMsg, params: list[str]):
    msg.reply("语音可用的人物列表:\n" + ", ".join(speakers))


@on_command("tts", param_len=-1,
            desc="文字转语音,如:tts 你好，"
                 "或:tts 可莉 你好",
            cmd_group_name="tts")
def tts_cmd(msg: GroupMsg | FriendMsg, params: list[str]):
    if len(params) == 0:
        msg.reply("请输入要转换的文字")
        return
    if len(params) > 1:
        text = " ".join(params[1:])
        speaker = params[0]
        if speaker not in speakers:
            msg.reply(f"没有 {speaker} 这个人物")
            return
    else:
        text = params[0]
        speaker = "可莉"

    max_len = 200
    if len(text) > max_len:
        msg.reply(f"文字长度超过{max_len}字")
        return
    try:
        data = tts(text, speaker)
    except Exception as e:
        msg.reply(f"语音转换失败: {e}")
        return
    msg.reply(MessageSegment.voice_base64(data))
