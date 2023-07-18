import unittest
from ..tusi import TusiDraw


class TestTusi(unittest.TestCase):

    def setUp(self) -> None:
        self.draw = TusiDraw()

    def test_txt2img(self):
        self.draw.txt2img("一个女孩在床上展示她的头发", print)
        input("drawing...")

    def test_get_models(self):
        print(self.draw.get_models())

    def test_set_model(self):
        print(self.draw.set_model("动漫"))

    def test_set_model_and_draw(self):
        self.test_set_model()
        self.test_txt2img()
