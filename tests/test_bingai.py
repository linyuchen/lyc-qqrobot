import unittest

from msgplugins.bingai.bingai_playwright import BingAIPlayWright


class TestBinAI(unittest.TestCase):
    def test_draw(self):
        res = BingAIPlayWright(proxy="http://localhost:7890", headless=False).draw("一只会飞的猫猫")
        print(res)


if __name__ == '__main__':
    unittest.main()
