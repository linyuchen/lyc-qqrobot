# -*- coding:UTF-8 -*-

import json
import requests

port = 6666
host = "http://localhost:%d" % (port)
login_url = "%s/login" % (host)

headers = {"Content-Type": "application/json"}
json_data = {"qq": "1412971608", "pwd": "neverlike"}
http = requests.session()
http.headers = headers
res = http.post(login_url, data=json.dumps(json_data))
print res.json()
