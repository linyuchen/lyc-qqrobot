import tempfile
import time

from pathlib import Path

import requests

base_path = Path(tempfile.mkdtemp())


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.106 Safari/537.36"}


def get_news2():
    base_path.mkdir(exist_ok=True)
    today = time.strftime("%Y-%m-%d")
    yesterday = time.strftime("%Y-%m-%d", time.localtime(time.time() - 24 * 60 * 60))
    today_img_path = base_path / (today + ".png")
    yesterday_img_path = base_path / (yesterday + ".png")

    if today_img_path.exists():
        # 对比昨天的图片，如果一样就不更新
        if yesterday_img_path.exists() and yesterday_img_path.stat().st_size == today_img_path.stat().st_size:
            today_img_path.unlink()
        else:
            return str(today_img_path)
    url = "http://dwz.2xb.cn/zaob"
    url = requests.get(url).json().get("imageUrl")
    if not url:
        return
    with open(today_img_path, "wb") as f:
        try:
            img_data = requests.get(url, headers=headers).content
            f.write(img_data)
            return str(today_img_path)
        except:
            return


if __name__ == '__main__':
    print(get_news2())
