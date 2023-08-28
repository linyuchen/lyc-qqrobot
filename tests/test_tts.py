import unittest

from msgplugins.tts.genshinvoice_top import tts as genshinvoice_top_tts
from msgplugins.tts.vits import tts as vits_tts


class TestVitsCase(unittest.TestCase):
    def test_vits(self):
        print(vits_tts("你好"))

    def test_gs(self):
        print(genshinvoice_top_tts("喵~你好呀，我是可莉喵", "可莉"))


if __name__ == '__main__':
    unittest.main()
