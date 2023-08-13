import tempfile
import threading
import time

from selenium.webdriver import ChromeOptions, Chrome

from config import TUSI_TOKENS


# options = ChromeOptions()


class Client:
    def __init__(self, url):
        options = ChromeOptions()
        tempdir = tempfile.mkdtemp()
        print(tempdir)
        options.add_argument(f"user-data-dir={tempdir}")
        self.driver = Chrome(options)
        self.url = url

    def start(self):
        self.driver.get(url=self.url)

    def set_cookie(self, cookie: str | dict):
        if isinstance(cookie, dict):
            # 将键值对用 =拼接
            cookie = ";".join([f"{k}={v}" for k, v in cookie.items()]) + ";"
        js = f"""
        const cookie = "{cookie}";
        function setCookie(){{
            document.cookie=`${{cookie}};` + "expires=" + new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toUTCString() + "; path=/" + ";domain=.tusi.art";
            location.reload();
        }}
        if (document.readyState === "complete") {{
            setCookie();
        }} else {{
          document.addEventListener("DOMContentLoaded", function() {{
            setCookie();
          }});
        }}
        setTimeout(() => {{
            setCookie();
        }}, 500);
        """
        self.driver.execute_script(js)

    def set_token(self, token: str):
        self.set_cookie({"ta_token_prod": token})


def start(token):
    client = Client(url="https://tusi.art/")
    client.start()
    client.set_token(token)
    while True:
        time.sleep(1)


for token in TUSI_TOKENS:
    threading.Thread(target=lambda: start(token)).start()
