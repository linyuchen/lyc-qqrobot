import unittest
from ..tusi import TusiDraw, MultipleCountPool


class TestTusi(unittest.TestCase):

    def setUp(self) -> None:
        self.draw = MultipleCountPool()

    def test_txt2img(self):
        while True:
            text = input("prompt: ")
            error = self.draw.txt2img(text, print)
            print(error)

    def test_get_models(self):
        print(self.draw.get_models())

    def test_set_model(self):
        print(self.draw.set_model("动漫"))

    def test_set_model_and_draw(self):
        self.test_set_model()
        self.test_txt2img()
