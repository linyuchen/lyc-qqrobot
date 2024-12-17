import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright


def login(url: str, data_path: Path=None, proxy: str='', ):
    data_path = data_path or tempfile.mkdtemp()
    browser_context_manager = sync_playwright().start()
    browser = browser_context_manager.chromium.launch_persistent_context(
        data_path,
        headless=False,
        base_url="",
        proxy={
            "server": proxy,
        } if proxy else None,
        args=["--enable-chrome-browser-cloud-management"]
    )
    browser.new_page().goto(url)

    input("login then press Enter to close...")
    browser_context_manager.stop()

