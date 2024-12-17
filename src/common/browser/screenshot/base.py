from contextlib import asynccontextmanager

from playwright.async_api import async_playwright

from src.common import DATA_DIR

CHROME_DATA_DIR = DATA_DIR / "playwright_screenshot"

@asynccontextmanager
async def new_page(url: str, proxy: str = "", headless=True):
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(CHROME_DATA_DIR, headless=headless, proxy={
            "server": proxy,
        } if proxy else None, viewport={"width": 1920, "height": 1080})
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=30000)
        except Exception as e:
            error_msg = f"{e}"
            pass
        yield page
        await page.close()
        await browser.close()
