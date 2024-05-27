import os
import re
from pathlib import Path


def get_electron_discord_token(appname="Midjourney"):
    # 获取用户的appdata路径
    appdata = os.getenv('APPDATA')
    leveldb_path = Path(appdata) / appname / "Local Storage" / "leveldb"
    # 找到所有.log文件
    log_files = [i for i in leveldb_path.glob("*.log")]
    # 按照文件名排序
    log_files.sort(key=lambda x: str(x))
    # 取最后一个
    log_file = log_files[-1]
    # 读取文件内容
    with open(log_file, "rb") as f:
        content = f.read()
        # 正则匹配token
        tokens = re.findall(rb'token.*"(.*?)"', content)
        return tokens[-1].decode()


if __name__ == '__main__':
    print(get_electron_discord_token())
