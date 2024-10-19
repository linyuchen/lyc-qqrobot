import asyncio
import tempfile
import time
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import quote

from PIL import Image
from playwright.async_api import async_playwright, Page

from src.common import DATA_DIR

CHROME_DATA_DIR = DATA_DIR / "playwright_screenshot"


@asynccontextmanager
async def new_page(url: str, proxy: str = "", headless=True) -> Page:
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


async def load_all(page: Page):
    result = await page.evaluate("""
        for(let i = 0; i <= document.body.scrollHeight; i+=500){
            setTimeout(function(){
                window.scrollTo(0, i);
                if (i >= (document.body.scrollHeight - 500)){

                    window.scrollTo(0, 0);
                }
            }, 200 * (i/500))
        }
        result = document.body.scrollHeight / 500
    """)
    time.sleep(result * 0.2)


