from .bv2_fastapi import BV2Fastapi
from .genshinvoice_top import tts as genshin_tts, speakers as genshin_speakers


class AutoSpeakerTTS:
    def __init__(self, bv2_fastapi_url: str):
        self.bv2 = BV2Fastapi(api_host=bv2_fastapi_url)
        self.default_speaker = "阿梓"
        self.max_text_len = 300

    def tts(self, text: str, speaker: str = ''):
        speaker = speaker or self.default_speaker
        bv2_speakers = self.bv2.get_models()
        if speaker in genshin_speakers:
            tts_func = genshin_tts
        elif speaker in bv2_speakers:
            tts_func = self.bv2.tts
        else:
            speaker = self.default_speaker
            tts_func = self.bv2.tts
            text = f"{speaker} {text}"

        if len(text) > self.max_text_len:
            raise Exception(f"文字长度超过{self.max_text_len}字")

        voice_path = tts_func(text, speaker)
        return voice_path
