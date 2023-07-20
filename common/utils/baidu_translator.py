# 百度翻译api
import hashlib

import requests


def sign(appid: str, q: str, salt: str, app_key):
    sign_str = appid + q + salt + app_key
    sign_result = hashlib.md5(sign_str.encode()).hexdigest()
    return sign_result


def trans(text: str, from_lang="zh", to_lang: str = "en"):
    # 百度翻译api
    # http://api.fanyi.baidu.com/api/trans/product/apidoc
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    app_id = "20191117000357769"
    app_key = "wKoSEHQiHenBgjfxJP5g"
    res = requests.post(url, data={
        "q": text,
        "from": from_lang,
        "to": to_lang,
        "appid": app_id,
        "salt": "1435660288",
        "sign": sign(app_id, text, "1435660288", app_key)}).json()

    if res.get("error_code") == "52001":
        return res.get("error_msg")

    return res["trans_result"][0]["dst"]


if __name__ == "__main__":
    r = trans("你好,世界，我在干嘛")
    print(r)

