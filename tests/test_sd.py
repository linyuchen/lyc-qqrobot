from unittest import TestCase

from msgplugins.stable_diffusion.sd import SDDraw
from msgplugins.tusi.tusi import TusiMultipleCountPool


class TestSD(TestCase):
    sd = SDDraw()

    def test_draw(self):
        res = self.sd.txt2img("1girl, sky, sunshine, flowers,鸟在天上飞")
        print(res)


class TestTusi(TestCase):
    def test_draw(self):
        TusiMultipleCountPool().txt2img("1girl", print)
