# -*- encoding:UTF8 -*-

import urllib2
import json

class Express:
    def __call__(self,param):
        """
        param: 公司名 空格 单号
        """

        express = {
        u'申通': 'shentong',
        u'EMS': 'ems',
        u'顺丰': 'shunfeng',
        u'圆通': 'yuantong',
        u'中通': 'zhongtong',
        u'韵达': 'yunda',
        u'天天': 'tiantian',
        u'汇通': 'huitongkuaidi',
        u'全峰': 'quanfengkuaidi',
        u'德邦': 'debangwuliu',
        u'宅急送': 'zhaijisong'
        }

        submit = u'快递查询'
        en = param.split(' ')
        if len(en) < 2:
            return u"命令错误！"
        ename, number = en
        if not express.has_key(ename):
            return u"目前还不支持 （%s） 这家公司的快递查询哦"%ename
        ename = express[ename]
        url = 'http://www.kuaidi100.com/query?type=%s&postid=%s&id=1&valicode=&temp=0.5542713834526946'%(ename, number)
        req = urllib2.urlopen(url).read()
        ret = json.loads(req)

        data = ret
#        print data
        rv = ''
        if data[u'message'] != 'ok':
            return data[u'message']
        data = data[u'data']
        data.reverse()
        for status in data:
            rv += status[u'time'] + ':'
            rv += status[u'context'] + '\n'
        return rv
