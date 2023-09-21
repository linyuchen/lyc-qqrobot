import tempfile
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.launch()


def search_baidu(keyword) -> Path:
    keyword = quote(keyword.encode("utf8"))
    page = browser.new_page()
    page.goto(f"https://www.baidu.com/s?wd={keyword}")
    e = page.locator("css=#content_left")
    e.evaluate("""
    e = document.getElementById("content_left")
    e.style.paddingLeft = "10px";
    e.style.paddingRight = "10px";
    """)
    path = Path(tempfile.mktemp(suffix=".png"))
    e.screenshot(path=path)
    page.close()
    return path

