from sqlalchemy import Column, String

from src.common.db.sqlalchemy import Base


class BlackUserList(Base):
    __tablename__ = "blacklist_user"
    target_id = Column(String, primary_key=True)


class BlackGroupList(Base):
    __tablename__ = "blacklist_group"
    target_id = Column(String, primary_key=True)
