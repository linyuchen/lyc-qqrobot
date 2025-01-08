from src.common.browser.login import login
from src.common.browser.screenshot.base import CHROME_DATA_DIR as SCREENSHOT_DATA_DIR

login("https://www.zhihu.com/signin", SCREENSHOT_DATA_DIR)