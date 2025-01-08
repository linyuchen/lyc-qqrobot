import asyncio
import tempfile
from pathlib import Path

from playwright.async_api import async_playwright, BrowserContext, Page


class BiliLogin:

    def __init__(self):
        self.browser: BrowserContext | None = None
        self.page: Page | None = None

    async def init(self):
        browser_context_manager = await async_playwright().start()
        self.browser = await browser_context_manager.chromium.launch_persistent_context(
            tempfile.mkdtemp(),
            headless=True)
        self.page = await self.browser.new_page()
        await self.page.goto("https://passport.bilibili.com/login")

    async def get_qrcode(self) -> Path:
        try:
            qrcode = await self.page.wait_for_selector(".login-scan")
        except Exception as e:
            raise TimeoutError("获取B站登录二维码超时")
        tmp_path = tempfile.mktemp(suffix=".png")
        await qrcode.screenshot(path=tmp_path)
        return Path(tmp_path)


    async def __get_cookie(self):
        cookies = await self.browser.cookies()
        cookie_parts = [f"{cookie['name']}={cookie['value']}" for cookie in cookies if "bilibili" in cookie["domain"]]
        cookies_text = "; ".join(cookie_parts)
        if "bili_jct" in cookies_text:
            return cookies_text

    async def get_cookie(self):
        for i in range(120):
            await asyncio.sleep(1)
            cookie = await self.__get_cookie()
            if cookie:
                return cookie
        raise TimeoutError("获取B站登录cookie超时")

    async def close(self):
        await self.page.close()
        await self.browser.close()


if __name__ == '__main__':
    async def main():
        bili_login = BiliLogin()
        await bili_login.init()
        qrcode_path = await bili_login.get_qrcode()
        print(qrcode_path)
        print(await bili_login.get_cookie())
        await bili_login.close()

    asyncio.run(main())