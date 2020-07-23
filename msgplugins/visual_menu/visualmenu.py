# coding=UTF8

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
        if not os.path.exists(self.allPath):
            os.mkdir(self.allPath)
        if not os.path.exists(self.adminPath):
            os.mkdir(self.adminPath)

        self.allFileList = []
        self.groupFileList = []
        self.adminFileList = []
        self.allMenu = {}  # key 文件名（去后缀），value 文件内的东东
        self.groupMenu = {}
        self.adminMenu = {}
        self.cmdNameList = []
        self.get_txts(self.allPath, self.allFileList, self.allMenu)
        self.get_txts(self.adminPath, self.adminFileList, self.adminMenu)
        self.get_txts(self.groupPath, self.groupFileList, self.groupMenu)

    def replace_value(self, txt_content):
        """
        处理txt里面的变量
        """
        for key, value in self.replaceValueDic.items():
            txt_content = txt_content.replace(key, value)

        return txt_content

    def get_txts(self, path, file_list, menu):

        _fileList = os.listdir(path)
        file_list[:] = [f for f in _fileList if f.endswith(self.ext)][:]
        for fileName in file_list:
            cmd_name = fileName[:- len(self.ext)]
            self.cmdNameList.append(cmd_name)
            with open(path + fileName, "rb") as f:
                data = f.read()
                data = self.replace_value(data.decode("utf8"))
                menu[cmd_name] = data
                f.close()


if __name__ == "__main__":

    test = VisualMenu()
    name = test.allMenu.keys()[0]
