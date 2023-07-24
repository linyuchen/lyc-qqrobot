import tempfile

import requests


def download2temp(url, suffix=""):
    res_f = requests.get(url).content
    tmp_path = tempfile.mktemp(suffix)
    with open(tmp_path, "wb") as f:
        f.write(res_f)
    return tmp_path


if __name__ == '__main__':
    p = download2temp(
        "https://tusi-images.oss-cn-shanghai.aliyuncs.com/workspace%2Fimages%2F615869302058359338%2Fe35fd282eaa8ded707ec2662df948812.png?Expires=1689717889&OSSAccessKeyId=LTAI5tA9wgpRFMZ23PwaJcL4&Signature=DfoIahIvSy69%2BPMA9TyuFQ8472A%3D",
        ".png")
    print(p)
