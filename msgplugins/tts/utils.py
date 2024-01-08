import subprocess
import tempfile
from pathlib import Path

from gradio_client.utils import encode_url_or_file_to_base64

from common.utils.downloader import download_file_with_progressbar

current_path = Path(__file__).parent
ffmpeg_path = current_path / "ffmpeg.exe"
silk_encoder_path = current_path / "silk_v3_encoder.exe"

if not ffmpeg_path.exists():
    ffmpeg_url = ("https://mirror.ghproxy.com/"
                  "https://github.com/linyuchen/qqrobot-plugin/releases/download/mmpeg/ffmpeg.exe")
    download_file_with_progressbar(ffmpeg_url, ffmpeg_path)


def wav2silk_base64(wav_path: Path) -> str:
    pcm_path = tempfile.mktemp(suffix=".pcm")
    silk_path = tempfile.mktemp(suffix=".silk")
    subprocess.call(f"{ffmpeg_path} -y -i {wav_path} -f s16le -ar 24000 -ac 1 {pcm_path}")
    subprocess.call(f"{silk_encoder_path} {pcm_path} {silk_path} -tencent -rate 8000")
    data = encode_url_or_file_to_base64(silk_path)
    return data


def wav2amr(wav_path: Path) -> Path:
    amr_path = tempfile.mktemp(suffix=".amr")
    pcm_path = tempfile.mktemp(suffix=".pcm")
    subprocess.call(f"{ffmpeg_path} -y -i {wav_path} -f s16le -ar 24000 -ac 1 {pcm_path}")
    subprocess.call(f"{silk_encoder_path} {pcm_path} {amr_path} -tencent")
    return Path(amr_path)
