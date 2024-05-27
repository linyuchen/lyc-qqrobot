
import sqlite3
from datetime import datetime
from src.common import DATA_DIR
from src.common.group_point import group_point_action


conn = sqlite3.connect(DATA_DIR / 'db2.sqlite3')

c = conn.cursor()

c.execute('''SELECT group_groupuser.*, account_myuser.qq, latest_time.max_time
FROM group_groupuser
INNER JOIN account_myuser ON group_groupuser.user_id = account_myuser.id
LEFT JOIN (
    SELECT user_id, MAX(time) as max_time
    FROM group_signrecord
    GROUP BY user_id
) latest_time ON group_groupuser.user_id = latest_time.user_id
;''')

data = c.fetchall()
for i in data:
    id_ = i[0]
    nick = i[1]
    group_qq = i[2]
    point: str = i[3]
    sign_continues = i[4]
    sign_count = i[6]
    qq: str = i[7]
    last_sign_time = i[8]

    member = group_point_action.get_member(group_qq, qq, nick)
    member.point = int(point)
    member.continuous_sign_count = sign_count
    member.total_sign_count = sign_count
    if last_sign_time:
        try:
            t = datetime.strptime(last_sign_time, "%Y-%m-%d %H:%M:%S")
        except:
            t = datetime.strptime(last_sign_time, "%Y-%m-%d %H:%M:%S.%f")
    else:
        t = None
    member.last_sign_date_time = t
    group_point_action.save()


print(data)