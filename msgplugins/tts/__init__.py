from msgplugins.msgcmd.cmdaz import on_command
from qqsdk.message import GroupMsg, FriendMsg, MessageSegment
from .genshinvoice_top import tts, speakers


@on_command("tts列表", param_len=0,
            desc="发送 tts列表 查看可用的人物列表",
            cmd_group_name="tts")
def tts_list(msg: GroupMsg | FriendMsg, params: list[str]):
    msg.reply("语音可用的人物列表:\n" + ", ".join(speakers))


@on_command("tts", param_len=-1,
            desc="发送 tts + 文字 进行语音转换,如:tts 你好\n"
                 "发送 tts + 人物 + 文字 进行文字转语音,如:tts 可莉 你好",
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

    if len(text) > 200:
        msg.reply("文字长度超过40字")
        return
    try:
        data = tts(text, speaker)
    except Exception as e:
        msg.reply(f"语音转换失败: {e}")
        return
    msg.reply(MessageSegment.voice_base64(data))
