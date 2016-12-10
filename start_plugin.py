# -*- coding:UTF-8 -*-

import sys

from qqsdk.main import Main

host = "localhost"
if len(sys.argv) > 1:
    port = sys.argv[1]
    port = int(port)
    if len(sys.argv) > 2:
        host = sys.argv[2]
else:
    port = 2999

Main(port, host).main()
