from pathlib import Path
from .predict import classify

cur_path = Path(__file__).parent

model_path = cur_path / "nsfw_mobilenet2.224x224.h5"

if not model_path.exists():
    raise Exception(f"nsfw检测模型{model_path}不存在，请下载模型放至{cur_path}, "
                    f"下载地址：https://s3.amazonaws.com/ir_public/ai/nsfw_models/nsfw.299x299.h5")

model = predict.load_model(model_path)


def nsfw_detect(img_path: Path) -> bool:
    data = classify(model, str(img_path))
    data = list(data.values())[0]
    return data["hentai"] > 0.5


__all__ = [
    "nsfw_detect"
]
