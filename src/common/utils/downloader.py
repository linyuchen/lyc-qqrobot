import tempfile
from pathlib import Path

import requests
from tqdm import tqdm


def download2temp(url, suffix="", http_proxy="") -> Path:
    res_f = requests.get(url, proxies={"http": http_proxy, "https": http_proxy} if http_proxy else {}).content
    tmp_path = tempfile.mktemp(suffix)
    with open(tmp_path, "wb") as f:
        f.write(res_f)
    return Path(tmp_path)


def download_file_with_progressbar(url: str, file_path: Path | str):
    print(f"download {url} to {file_path}")
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kilobyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(file_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")


if __name__ == '__main__':
    download_file_with_progressbar("https://s3.amazonaws.com/ir_public/nsfwjscdn/nsfw_mobilenet2.224x224.h5", "./nsfw.h5")

