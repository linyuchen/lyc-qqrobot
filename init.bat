call venv/scripts/activate
set PYTHONPATH=%~dp0
playwright install chromium
meme download
python scripts/init.py
python config.py
