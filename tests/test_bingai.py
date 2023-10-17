import unittest

from msgplugins.bingai.bingai_playwright import BingAIPlayWright, BinAITaskPool, BingAIChatTask

chat_pool = BinAITaskPool(proxy="http://localhost:7890", headless=False)
chat_pool.start()


class TestBingAI(unittest.TestCase):

    def test_chat(self):
        while True:
            uid = input("user_id:")
            question = input("请输入问题：")
            print("思考中...")
            chat_pool.put_task(BingAIChatTask(uid, question, print))

    def test_draw(self):
        res = BingAIPlayWright(proxy="http://localhost:7890", headless=False).draw("一直会飞的猫")
        print(res)


if __name__ == '__main__':
    unittest.main()
