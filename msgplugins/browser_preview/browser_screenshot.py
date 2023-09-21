import tempfile
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

p = None
browser = None


def get_browser():
    global browser
    if browser:
        return browser
    else:
        global p
        p = sync_playwright().start()
        browser = p.chromium.launch()
        return browser


def search_baidu(keyword) -> Path:
    keyword = quote(keyword.encode("utf8"))
    page = get_browser().new_page()
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

