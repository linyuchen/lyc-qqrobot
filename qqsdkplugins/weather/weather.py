# -*- encoding:UTF8 -*-
import urllib2
import urllib
from xml.etree import ElementTree


class Weather:

    def __init__(self):

        self.weather_info_list = [(u"城市", "city"), (u"发布日期", "savedate_weather"), (u"天气概况", "status1"),
                                  (u"风向", "direction1"), (u"风级", "power1"), (u"最高温度", "temperature1"),
                                  (u"最低温度", "temperature2"), (u"穿衣说明", "chy_shuoming"),
                                  (u"污染程度", "pollution_l"), (u"紫外线", "zwx_s"), (u"舒适度", "ssd_s"),
                                  (u"空调", "ktk_s"), (u"洗车", "xcz_s"), (u"感冒", "gm_s"), (u"运动", "yd_s")]

        self.tomorrow_weather_info_list = [(u"天气概况", "status1"), (u"风向", "direction1"),
                                           (u"风级", "power1"), (u"最高温度", "temperature1"),
                                           (u"最低温度", "temperature2")]

    @staticmethod
    def parse_xml(xml, info_list):

        info = ""
        root = ElementTree.fromstring(xml.encode("u8"))
        
        weather = root.find("Weather")
        if not weather:
            return u"没有找到您要查询的地名天气"
        for weather_info in info_list:
            text = weather.find(weather_info[1]).text
            if not text:
                continue
            info += weather_info[0] + u"：" + text + "\n"
        return info

    def get_info(self, day, info_list):
        info = ""
        url = "http://php.weather.sina.com.cn/xml.php?city=%s&password=DJOYnieT8234jlsK&day=%d" % \
              (self.city, day)
        res = urllib2.urlopen(url).read().decode("u8")
        info += self.parse_xml(res, info_list)
        return info
    
    def __call__(self, city):

        city = city.encode("gbk")
        city = urllib.quote(city)
        self.city = city
        result = self.get_info(0, self.weather_info_list)
        result += u"\n\n明日天气：\n" + self.get_info(1, self.tomorrow_weather_info_list)

        return result

if __name__ == "__main__":

    test = Weather()
    print test(u"北京")
