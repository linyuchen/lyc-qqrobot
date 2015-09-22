#coding=UTF8

"""
"""
import os
import locale
class VisualMenu(object):

    def __init__(self):
        super(VisualMenu, self).__init__()

        # key  txt的原始内容
        # value 要替换的内容
        self.replaceValueDic = {"{robot_name}": u"喵喵咪"} 
        self.ext = ".txt"
        self.curPath = os.path.dirname(__file__)
        self.encoding = locale.getdefaultlocale()[1]
        if not self.curPath:
            self.curPath = "."
        self.curPath += "/menutxt/"
        self.allPath = self.curPath + "all/"
        self.groupPath = self.curPath + "group/"
        self.adminPath = self.curPath + "admin/"
        self.allFileList = []
        self.groupFileList = []
        self.adminFileList = []
        self.allMenu = {} # key 文件名（去后缀），value 文件内的东东
        self.groupMenu = {}
        self.adminMenu = {}
        self.cmdNameList = []
        self.getTxts(self.allPath, self.allFileList, self.allMenu)
        self.getTxts(self.adminPath, self.adminFileList, self.adminMenu)
        self.getTxts(self.groupPath, self.groupFileList, self.groupMenu)

    def replaceValue(self, txtContent):
        """
        处理txt里面的变量
        """
        for key, value in self.replaceValueDic.items():
            txtContent = txtContent.replace(key, value)

        return txtContent

    def getTxts(self, path, fileList, menu):

        _fileList = os.listdir(path)
        fileList[:] = [f for f in _fileList if f.endswith(self.ext)][:]
#        self.cmdNameList = [f[: - len(self.ext)].decode(self.encoding) for f in fileList if f.endswith(self.ext)]
        for fileName in fileList:
            cmdName = fileName[:- len(self.ext)].decode(self.encoding)
            self.cmdNameList.append(cmdName)
            with open(path + fileName) as f:
                data = f.read().decode("u8")
                data = self.replaceValue(data)
                menu[cmdName] = data
                f.close()


if __name__ == "__main__":

    test = VisualMenu()
    name = test.allMenu.keys()[0]
    print test.allMenu[u"1.2"]
    print test.cmdNameList
