"venv/scripts/activate && "
set PYTHONPATH=%~dp0
playwright install chromium
meme download
python src/common/bingai/login.py
python src/common/bilicard/login.py
python src/common/webpage_screenshot.py
python config.py

