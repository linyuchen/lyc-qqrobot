#coding=UTF8

"""
命令解析模块
"""


class CMD(object):
    
    def __init__(self, cmdName, hasParam=False, paramSep=" "):
        """
        hasParam: 是否需要参数
        paramSep: 命令与参数的分隔符，同时也是多个参数之间的分隔符
            如果为None 或者 False则不分割
        """

        self.cmdName = cmdName
        self.hasParam = hasParam
        self.paramSep = paramSep
        self.paramList = []

    def az(self, originalCmd):
        """
        解析命令
        成功返回True，反之False
        """

        self.originalCmd = originalCmd

        if self.hasParam: # 需要参数，进行参数分割
            cmdNameLength = len(self.cmdName)
            if len(originalCmd) <= cmdNameLength: # 如果没有参数
                return False

            if self.paramSep == " ":
                self.paramList = originalCmd.split()
            elif self.paramSep:
                self.paramList = originalCmd.split(self.paramSep)

            if self.paramList:
                cmdName = self.paramList[0]
                self.paramList.pop(0)
                if not self.paramList:
                    return False
                self.originalParam = self.paramSep.join(self.paramList)

            if not self.paramSep:#无分隔符
                self.paramList = [originalCmd[cmdNameLength: ]]
                cmdName = originalCmd[:cmdNameLength]
                self.originalParam = self.paramList[0]
        else:
            cmdName = originalCmd
            
        if cmdName != self.cmdName:
            return False

        return True

    def getParamList(self):
        """
        :return: 参数列表
        """

        return self.paramList

    def getOriginalParam(self):
        """
        :return: 除了命令部分剩下的参数字符串
        """
        return self.originalParam

if "__main__" == __name__:
    cmd = CMD(u"命令1")
    print cmd.az(u"命令1")

    cmd = CMD(u"天气", hasParam=True)
    print cmd.az(u"天气 绵阳")
    print  cmd.getParamList()
    print cmd.originalParam
    cmd = CMD(u"命令3", hasParam=True, paramSep=None)
    print cmd.az(u"命令3 fadsfa")
    print cmd.getParamList()
    print cmd.originalParam
