import tempfile

from playwright.sync_api import sync_playwright

CHROME_DATA_DIR = tempfile.gettempdir() + "/playwright_chrome_data_bingai"


class BingAIPlayWright:

    def __init__(self, proxy: str = "", headless=True):
        with sync_playwright() as p:
            self.browser = p.chromium.launch_persistent_context(CHROME_DATA_DIR, headless=headless, proxy={
                "server": proxy,
            } if proxy else None)
            self.page = self.browser.new_page()
            url = "https://www.bing.com/chat?cc=us"
            try:
                self.page.goto(url, timeout=30000)
            except Exception as e:
                error_msg = f"{e}"

        self.question_num = 0

    def send_msg(self, msg: str):
        self.page.fill("textarea", msg)
        self.page.click("div[class='control submit']")
        self.question_num += 1

    def get_msg(self):
        id = "stop-responding-button"  # 判断这个是否是disable
        return self.page.query_selector("div[class='message message-from-me']").inner_text()
