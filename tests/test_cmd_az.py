import unittest

from msgplugins.msgcmd.cmdaz import CMD


class TestCMDCase(unittest.TestCase):
    def test_0args(self):
        test_cmd = CMD("mj", param_len=0)
        result = test_cmd.az("mj")
        self.assertEqual(result, [""])
        result = test_cmd.az("mk")
        self.assertEqual(result, False)

    def test_1args(self):
        test_cmd = CMD("mj", param_len=1)
        result = test_cmd.az("mj <lora:op>,keqing --ar 16:9")
        print(result)

    def test_az_args(self):
        test_cmd = CMD("mj", param_len=-1)
        result = test_cmd.az("mj")
        self.assertEqual(result, [""])
        result = test_cmd.az("mj a")
        self.assertEqual(result, ["a"])
        result = test_cmd.az("mj a \nb")
        self.assertEqual(result, ["a", "\nb"])


if __name__ == '__main__':
    unittest.main()
