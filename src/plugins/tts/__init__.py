import traceback

from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin.on import on_command

from config import get_config
from .genshinvoice_top import tts, speakers
from .auto_speaker import AutoSpeakerTTS
from .utils import wav2amr

auto_speaker_tts = AutoSpeakerTTS(get_config("BV2_FASTAPI"))

tts_list_cmd = on_command("tts列表")


@tts_list_cmd.handle()
def _():
    tts_list_cmd.finish("语音可用的人物列表:\n" + ", ".join(speakers + auto_speaker_tts.bv2.get_models()))


tts_cmd = on_command("tts")


@tts_cmd.handle()
async def _(args: Message = CommandArg()):
    params = args.extract_plain_text().split()
    if len(params) == 0:
        tts_cmd.finish("tts后面需要接空格和文字")
        return

    speaker = ""
    if len(params) > 1:
        speaker = params[0]
        text = " ".join(params[1:])
    else:
        text = params[0]
    try:
        voice_path = auto_speaker_tts.tts(text, speaker)
        await tts_cmd.send(MessageSegment.record(voice_path))
    except Exception as e:
        traceback.print_exc()
        await tts_cmd.send(str(e))
    await tts_cmd.finish()
