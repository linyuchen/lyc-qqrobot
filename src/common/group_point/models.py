from pytz import timezone
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

from src.common import DATA_DIR

cn_timezone = timezone('Asia/Shanghai')

Base = declarative_base()


class GroupMember(Base):
    __tablename__ = 'group_members'
    qq = Column(String, primary_key=True)  # 在 TG 或者别的平台它是 userid
    username = Column(String, nullable=True, default=None)  # QQ 没这个字段
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
