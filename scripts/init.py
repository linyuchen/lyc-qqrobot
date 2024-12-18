import asyncio
import time
from src.common.browser.login import login
from src.common.browser.screenshot.base import CHROME_DATA_DIR as SCREENSHOT_DATA_DIR
from src.common.bilicard.login import login as bili_login

print('开始登录知乎，用于知乎截图插件')
login("https://www.zhihu.com/signin", SCREENSHOT_DATA_DIR)

print('开始登录B站，用于B站视频解析插件')
asyncio.run(bili_login())

print('开始登录微软Copilot，如不需要此插件直接关掉浏览器窗口即可')
time.sleep(3)
login("https://copilot.microsoft.com", SCREENSHOT_DATA_DIR)