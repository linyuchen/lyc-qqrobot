# coding: UTF8

import os


class PyRun:

    def __init__(self):
        pass

    def run(self, cmd_str, m=True):
        """
        m: 是否有模块
        """

        blank_pos = cmd_str.find(" ")
        if m:
            module = cmd_str[:blank_pos]
            code_str = cmd_str[blank_pos + 1:]
            code_str = "import %s;"%(module) + code_str
        else:
            code_str = cmd_str

        code_str = code_str.replace('"',"'")
        code_str = "python -c \"%s\""%code_str
#        print code_str
        p = os.popen(code_str)
        result = p.read()
        result = result[:500]
        return result.decode("gbk")

    def __call__(self, cmd_str, m=True):
        
        return self.run(cmd_str, m)

if __name__ == "__main__":

    test = PyRun()
#    print test.run("import time;help(time.localtime)")
    print test("time print dir(time)")
    s = raw_input("code:")
    print test(s,True)

        
