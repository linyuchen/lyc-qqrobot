from datetime import datetime, timedelta

from pytz import timezone
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

from src.common import DATA_DIR

cn_timezone = timezone('Asia/Shanghai')

Base = declarative_base()


class GroupMember(Base):
    __tablename__ = 'group_members'
    qq = Column(String, primary_key=True)
    nick = Column(String)
    point = Column(Integer, default=0)
    total_sign_count = Column(Integer, default=0)
    continuous_sign_count = Column(Integer, default=0)
    last_sign_date_time = Column(DateTime(timezone=True), nullable=True, default=None)
    group_qq = Column(String, ForeignKey('groups.qq'), primary_key=True)
    group = relationship("Group", back_populates="members")


class Group(Base):
    __tablename__ = 'groups'
    qq = Column(String, primary_key=True)
    members = relationship("GroupMember", back_populates="group", cascade="all, delete, delete-orphan")


# 数据库配置
db_path = DATA_DIR / 'group_point.db'
engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)  # 创建表
Session = sessionmaker(bind=engine)
session = Session()


# 示例: 添加数据到数据库
# group = Group(id='group1')
# member = GroupMember(qq='12345', point=10, total_sign_count=5, continuous_sign_count=3, last_sign_date=date.today(), group=group)
# session.add(group)
# session.add(member)
# session.commit()

# 查询示例
# group_query = session.query(Group).filter_by(id='group1').first()
# print(group_query)


class GroupPointAction:
    SIGN_POINT = 2000
    CONTINUOUS_SIGN_POINT = 100  # 连续签到一次获得的积分
    POINT_NAME = '活跃度'

    def save(self):
        session.commit()

    def get_member(self, group_qq: str, member_qq: str, nick: str = None) -> GroupMember:
        member = session.query(GroupMember).filter_by(group_qq=group_qq, qq=member_qq).one_or_none()
        if not member:
            return self.__add_member(group_qq, member_qq, nick or member_qq)
        if member.nick != nick and nick:
            member.nick = nick
            session.commit()
        return member

    def __add_member(self, group_qq: str, member_qq: str, nick: str):
        group = session.query(Group).filter_by(qq=group_qq).first()
        if not group:
            group = self.__add_group(group_qq)
        member = GroupMember(qq=member_qq, nick=nick, group_qq=group_qq)
        session.add(member)
        session.commit()
        return member

    def __add_group(self, group_qq: str):
        group = Group(qq=group_qq)
        session.add(group)
        session.commit()
        return group

    def sign(self, group_qq: str, member_qq: str, nick: str):
        member = self.get_member(group_qq, member_qq, nick)
        now = datetime.now(cn_timezone)
        today = now.date()
        if member.last_sign_date_time:
            last_sign_date = member.last_sign_date_time.date()
            if last_sign_date == today:
                return f'今天已经签到过了\n连续签到{member.continuous_sign_count}次\n总共签到{member.total_sign_count}次'

            # 判断是否是连续签到
            td = today - last_sign_date
            if td == timedelta(days=1):
                member.continuous_sign_count += 1
            else:
                member.continuous_sign_count = 1
        else:
            member.continuous_sign_count = 1
            last_sign_date = None

        last_sign_date_str = last_sign_date.strftime('%Y-%m-%d') if last_sign_date else '无'
        reward_point = self.SIGN_POINT + (member.continuous_sign_count - 1) * 100
        member.point += reward_point
        member.last_sign_date_time = now
        member.total_sign_count += 1
        session.commit()
        return f'签到成功，获得{reward_point}{self.POINT_NAME}\n上次签到{last_sign_date_str}\n连续签到{member.continuous_sign_count}次\n一共签到{member.total_sign_count}次'

    def add_point(self, group_qq: str, member_qq: str, point: int):
        member = self.get_member(group_qq, member_qq)
        member.point += int(point)
        session.commit()
        return member.point

    def transfer_point(self, group_qq: str, my_qq: str, other_qq: str, point: int):
        point = int(abs(point))
        other_user = session.query(GroupMember).filter_by(group_qq=group_qq, qq=other_qq).one_or_none()
        me = self.get_member(group_qq, my_qq)
        if not other_user:
            return "对不起，您要转账的对象不存在！请先让他在群里签到。"
        rest_point = me.point
        if point > rest_point:
            return "对不起，您的余额不够要转的额度！"
        if other_user.qq == me.qq:
            return "自己转给自己闲得慌吗"
        me.point -= point
        other_user.point += point
        session.commit()
        return "转账成功"

    def __get_point_rank(self, group_qq: str):
        """
        :return: users
        :rtype: list
        """
        users = session.query(GroupMember).filter(GroupMember.group_qq == group_qq).order_by(
            GroupMember.point.desc()).limit(10).all()
        return users

    def __get_point_rank_index(self, group_qq: str, member_qq: str):
        member_point = self.get_member(group_qq, member_qq).point
        rank_index = session.query(func.count(GroupMember.qq)).filter(
            GroupMember.point > member_point,
            GroupMember.group_qq == group_qq).scalar() + 1
        return rank_index

    def get_point_info(self, group_qq: str, member_qq: str) -> str:
        member = self.get_member(group_qq, member_qq)
        return f'{self.POINT_NAME}：{member.point}，当前排名：{self.__get_point_rank_index(group_qq, member_qq)}'

    def get_point_rank(self, group_qq: str):
        users = self.__get_point_rank(group_qq)
        result = ""
        for index, user in enumerate(users):
            item = f"{index + 1}. {user.nick}: {user.point}\n"
            result += item
            # result += "第%d名：%s(%s)，%s\n" % \
            #           (index + 1, user.nick, user.user.qq, user.get_point())

        return result


group_point_action = GroupPointAction()

__all__ = ['group_point_action']

if __name__ == '__main__':
    # m = group_point_action.get_member("1", "379450327")
    # print(m)
    test_group_qq = "1"
    test_qq = "11"
    test_qq2 = "22"
    print(group_point_action.sign(test_group_qq, test_qq, "啥"))
    print(group_point_action.sign(test_group_qq, test_qq2, "啥2"))
    group_point_action.add_point(test_group_qq, test_qq, 2000)
    print(group_point_action.transfer_point(test_group_qq, test_qq, test_qq2, 2000))
    print(group_point_action.get_point_rank(test_group_qq))
    print(group_point_action.get_point_info(test_group_qq, test_qq))
