import unittest
from pathlib import Path

import requests

from msgplugins.tts.genshinvoice_top import tts as genshinvoice_top_tts
from msgplugins.tts.bv2_fastapi import BV2Fastapi
from msgplugins.tts.utils import wav2amr
# from msgplugins.tts.vits import tts as vits_tts


class TestVitsCase(unittest.TestCase):
    # def test_vits(self):
    #     print(vits_tts("你好"))

    def test_gs(self):
        print(genshinvoice_top_tts("喵你好呀，我是可莉喵,おはよう", "可莉"))

    def test_bv2(self):
        bv2 = BV2Fastapi()
        wav_path = bv2.tts("我给你一个大逼兜", "嘉然")
        print(wav2amr(wav_path))

    def test_wav2amr(self):
        print(wav2amr(Path(r"d:\1.wav"), Path(r"d:\1.amr")))


if __name__ == '__main__':
    unittest.main()
