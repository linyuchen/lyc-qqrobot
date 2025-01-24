from sqlalchemy import Column, String, JSON
from sqlalchemy.ext.mutable import MutableList

from src.db.models.base import Base


class GroupIgnoreCMD(Base):
    __tablename__ = "group_ignore_cmd"
    group_id = Column(String, primary_key=True)
    cmds = Column(MutableList.as_mutable(JSON), default=lambda: [])
