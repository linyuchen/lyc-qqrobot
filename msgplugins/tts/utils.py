import subprocess
import tempfile
from pathlib import Path

from gradio_client.utils import encode_url_or_file_to_base64


def wav2silk_base64(wav_path: Path) -> str:
    pcm_path = tempfile.mktemp(suffix=".pcm")
    silk_path = tempfile.mktemp(suffix=".silk")
    current_path = Path(__file__).parent
    subprocess.call(f"{current_path}/ffmpeg -y -i {wav_path} -f s16le -ar 24000 -ac 1 {pcm_path}")
    subprocess.call(f"{current_path}/silk_v3_encoder.exe {pcm_path} {silk_path} -tencent")
    data = encode_url_or_file_to_base64(silk_path)
    return data
