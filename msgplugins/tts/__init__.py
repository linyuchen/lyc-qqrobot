from pathlib import Path

from msgplugins.msgcmd.cmdaz import on_command
from qqsdk.message import GroupMsg, FriendMsg, MessageSegment
from config import get_config
from .bv2_fastapi import BV2Fastapi
from .genshinvoice_top import tts, speakers
from .utils import wav2amr

bv2 = BV2Fastapi(api_host=get_config("BV2_FASTAPI"))


def bv2_tts(text: str, speaker: str) -> Path:
    wav_path = bv2.tts(text, speaker)
    return wav2amr(wav_path)


@on_command("tts列表", param_len=0,
            desc="获取文字转语音角色列表",
            cmd_group_name="tts")
def tts_list(msg: GroupMsg | FriendMsg, params: list[str]):
    msg.reply("语音可用的人物列表:\n" + ", ".join(speakers + bv2.get_models()))


@on_command("tts", param_len=-1,
            desc="文字转语音, 可以指定角色声音",
            example="tts 你好 或 tts 可莉 你好",
            cmd_group_name="tts")
def tts_cmd(msg: GroupMsg | FriendMsg, params: list[str]):
    default_speaker = "阿梓"
    if len(params) == 0:
        msg.reply("请输入要转换的文字")
        return

    text = params[0]
    speaker = default_speaker
    tts_func = tts
    if len(params) > 1:
        user_speaker = params[0]
        bv2_speakers = bv2.get_models()
        if user_speaker in speakers + bv2_speakers:
            speaker = user_speaker
            text = " ".join(params[1:])
            if user_speaker in bv2_speakers:
                tts_func = bv2_tts
        else:
            text = " ".join(params)

    max_len = 200
    if len(text) > max_len:
        msg.reply(f"文字长度超过{max_len}字")
        return
    try:
        voice_path = tts_func(text, speaker)
    except Exception as e:
        msg.reply(f"语音转换失败: {e}")
        return
    msg.reply(MessageSegment.voice_path(voice_path))
