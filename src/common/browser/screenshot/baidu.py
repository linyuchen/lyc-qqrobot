import tempfile
from pathlib import Path
from urllib.parse import quote

from src.common.browser.screenshot.base import new_page


async def screenshot_search_baidu(keyword: str) -> Path:
    keyword = quote(keyword.encode("utf8"))

    url = f"https://www.baidu.com/s?wd={keyword}"
    async with new_page(url) as page:
        e = page.locator("css=#content_left")
        await e.evaluate("""
        e = document.getElementById("content_left")
        e.style.paddingLeft = "10px";
        e.style.paddingRight = "10px";
        document.getElementById("head").style.display="none";
        try{
            document.getElementById("searchTag").style.display="none";
        }catch{}
        """)
        path = Path(tempfile.mktemp(suffix=".png"))
        await e.screenshot(path=path)
        await page.close()
        return path
