#coding:UTF8

import time
import sys
import traceback
sys.path.append("..")
import sqliteclient
qqsqlite = sqliteclient.Sqlite("qqgroup.db")
msqlite = sqliteclient.Sqlite("group_manager.db")

t_point = "t_point"

memberInfo = qqsqlite.get_value("t_group", ["group_qq_number", "qq_number", "point", "name", "sign_date", "sign_count", "continuous_sign_count"])
#memberInfo = memberInfo[:]
#print memberInfo
st = time.time()
length = len(memberInfo)
i = 0
for info in memberInfo:
    i += 1
    print i, length, time.time() - st,
    group_qq = info[0]
    member_qq = info[1]
    point = info[2]
    name = info[3]
    sign_date = info[4]
    sign_total = info[5]
    sign_continuous = info[6]
    #print sign_date
    #print group_qq, member_qq

    try:
        if eval(point) <= 0 or point == "99999999999999999" or not name:
            print "pass"
        else:
            msqlite.set_value(t_point, {"group_qq": group_qq, 
        "member_qq": member_qq, "point": point, "name": name}, 
        {"group_qq": group_qq,
            "member_qq": member_qq})

        if sign_date == "1970-01-02" or not sign_date:
            print "pass"
        else:
            msqlite.set_value("t_sign", {"group_qq": group_qq,
        "member_qq": member_qq, "sign_date": sign_date, "total": sign_total,
        "continuous": sign_continuous}, {"group_qq": group_qq,
            "member_qq": member_qq})
    except:
        print info
        traceback.print_exc()
