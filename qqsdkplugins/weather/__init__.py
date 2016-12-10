# coding=UTF8

"""
天气查询插件
"""
import weather
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
weather = weather.Weather()


class WeatherEvent(MsgEvent):
    __doc__ = u"""
    """

    def __init__(self):

        super(WeatherEvent, self).__init__()
        self.name = "weather"
        self.cmd = CMD(u"天气", param_len=1)

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        if self.cmd.az(msg.msg):
            result = weather(self.cmd.get_param_list()[0])
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    Name = u"天气"

    def install(self):

        event = WeatherEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addFriendMsgEvent(event)

        print u"插件【%s】被安装了" % self.Name

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.Name
