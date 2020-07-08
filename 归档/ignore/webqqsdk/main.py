# -*-coding: UTF8-*-

import sys
import qqclient 
sys.path.append("..")
import qqsdk

class Main(qqsdk.Main, qqclient.QQClient):

    def __init__(self, qq, pwd):
        qqsdk.Main.__init__(self)
        qqclient.QQClient.__init__(self, qq, pwd)


qq = sys.argv[1]
pwd = sys.argv[2]
robot = Main(qq, pwd)
robot.main()
