import asyncio
import unittest

from msgplugins.bingai.bingai_playwright import BingAIPlayWright, BinAITaskPool, BingAIChatTask, BingAIDrawTask

bingai_pool = BinAITaskPool(proxy="http://localhost:7890", headless=False)
bingai_pool.start()


class TestBingAI(unittest.TestCase):

    def test_chat(self):
        while True:
            uid = input("user_id:")
            question = input("请输入问题：")
            print("思考中...")
            bingai_pool.put_task(BingAIChatTask(uid, question, print))

    def test_draw(self):
        async def t():
            p = await BingAIPlayWright(proxy="http://localhost:7890", headless=False).init()
            result = await p.draw("青椒炒肉")
            print(result)
        # asyncio.run(t())
        # input("按任意键退出")
        bingai_pool.put_task(BingAIDrawTask("丧尸大战老鼠", print))
        bingai_pool.join()


if __name__ == '__main__':
    unittest.main()
