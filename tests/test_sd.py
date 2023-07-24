from unittest import TestCase

from msgplugins.stable_diffusion.sd import SDDraw


class TestSD(TestCase):
    sd = SDDraw()

    def test_draw(self):
        res = self.sd.txt2img("1girl, sky, sunshine, flowers,鸟在天上飞，阴部")
        print(res)
