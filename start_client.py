# -*- coding:UTF-8 -*-


import sys

from jsonapi_httpsrv import main


qq = sys.argv[1]
pwd = sys.argv[2]
port = sys.argv[3]
port = int(port)

main.main(qq, pwd, port)
