import asyncio

from common import PLAYWRIGHT_DATA_DIR
from config import get_config
from msgplugins.bingai.bingai_playwright import BingAIPlayWright


async def login():
    bingai = await BingAIPlayWright(proxy=get_config("GFW_PROXY"), headless=False,
                                    data_path=PLAYWRIGHT_DATA_DIR).init()
    page = await bingai.new_page()
    await page.goto("https://login.live.com/")
    input("login Microsoft then press Enter to continue...")
    await bingai.browser_context_manager.stop()


if __name__ == '__main__':
    asyncio.run(login())
