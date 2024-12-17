import asyncio
import tempfile
from pathlib import Path

from src.common.browser.playwright import load_all
from src.common.browser.screenshot.base import new_page


async def screenshot_moe_wiki(keyword: str) -> Path | None:
    async with new_page(f"https://zh.moegirl.org.cn/{keyword}") as page:
        close_btn = page.locator("css=.n-base-close.n-base-close--absolute.n-card-header__close")
        if await close_btn.count() > 0:
            await close_btn.first.click()
            await asyncio.sleep(1)
        await load_all(page)
        content = await page.query_selector("#mw-content-text")
        if not content:
            return
        await content.evaluate(
            """
            e = document.getElementById("mw-content-text")
            e.style.paddingLeft = "40px";
            e.style.paddingRight = "40px";
            """
        )
        path = Path(tempfile.mktemp(suffix=".png"))
        await content.screenshot(path=path)
        await page.close()
        return path
