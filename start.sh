cd /home/linyuchen/qqrobot-plugin
source "venv/bin/activate"
ps aux | grep '1577491075' | awk '{print $2}' | xargs kill -9
python ./client/mirai_http/main.py 1577491075