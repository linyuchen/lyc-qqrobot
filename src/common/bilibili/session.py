import re

import httpx

from src.common import DATA_DIR

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/107.0.0.0 Mobile Safari/537.36 Edg/107.0.1418.35",
    "Referer": "https://www.bilibili.com/",
    "Accept": "application/json;charset=UTF-8"
}
COOKIE_PATH = DATA_DIR / "bili_cookie.txt"
session = httpx.AsyncClient(headers=headers, follow_redirects=True)


def parse_cookie(cks: str):
    _cookies = re.findall("(.*?)=(.*?); ", cks)
    _cookies = dict(_cookies)
    return _cookies


def set_bili_cookie(cks: str):
    COOKIE_PATH.write_text(cks)
    session.cookies = parse_cookie(cks)


if COOKIE_PATH.exists():
    session.cookies = parse_cookie(COOKIE_PATH.read_text())
