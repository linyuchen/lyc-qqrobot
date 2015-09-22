# -*- coding:UTF-8 -*-

import sys

from qqsdk.main import Main

if len(sys.argv) > 1:
    port = sys.argv[1]
    port = int(port)
else:
    port = 666
Main(port).main()
