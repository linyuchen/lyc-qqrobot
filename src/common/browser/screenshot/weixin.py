import tempfile
from pathlib import Path

from src.common.browser.playwright import load_all
from src.common.browser.screenshot.base import new_page


async def screenshot_wx_article(url: str) -> Path | None:
    async with new_page(url) as page:
        content = page.locator("css=#img-content")
        if content.count() == 0:
            return
        await load_all(page)
        await content.evaluate(
            """
            e = document.getElementById("img-content")
            e.style.paddingLeft = "40px";
            e.style.paddingRight = "40px";
            """
        )
        path = Path(tempfile.mktemp(suffix=".png"))
        await content.screenshot(path=path)
        await page.close()
        return path
