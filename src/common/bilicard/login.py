import asyncio

from playwright.async_api import async_playwright

from src.common import PLAYWRIGHT_DATA_DIR
from src.common.bilicard.bilicard import COOKIE_PATH


async def login():
    async with async_playwright() as browser_context_manager:
        browser = await browser_context_manager.chromium.launch_persistent_context(
            PLAYWRIGHT_DATA_DIR,
            headless=False)
        page = await browser.new_page()
        await page.goto("https://passport.bilibili.com/login")
        while True:
            await asyncio.sleep(1)
            cookies = await browser.cookies()
            cookie_parts = [f"{cookie['name']}={cookie['value']}" for cookie in cookies if "bilibili" in cookie["domain"]]
            cookies_text = "; ".join(cookie_parts)
            if "bili_jct" in cookies_text:
                cookie_path = COOKIE_PATH
                cookie_path.write_text(cookies_text)
                break
        await page.close()
        await browser.close()


if __name__ == '__main__':
    asyncio.run(login())
