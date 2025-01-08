import asyncio
import unittest
from src.common.browser.screenshot.zhihu import ZhihuPreviewer, ZhihuLogin


class TestZhihu(unittest.TestCase):

    def test_login(self):
        zhihu_login = ZhihuLogin()

        async def main():
            await zhihu_login.init()
            qrcode_path = await zhihu_login.get_qrcode()
            print(qrcode_path)
            login_result = await zhihu_login.check_login()
            assert login_result == True

        asyncio.run(main())

    def test_previewer(self):
        zhihu_previewer = ZhihuPreviewer()

        async def main():
            result = await zhihu_previewer.screenshot_zhihu_question("https://www.zhihu.com/question/535225379")
            print(result)

        asyncio.run(main())


if __name__ == '__main__':
    unittest.main()
