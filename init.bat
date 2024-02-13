"venv/scripts/activate"
set PYTHONPATH=%~dp0
playwright install chromium
meme download
python msgplugins/bingai/login.py
python msgplugins/bilicard/login.py
python msgplugins/browser_preview/browser_screenshot.py
python config.py
cd msgplugins/superplugin
python manage.py migrate
