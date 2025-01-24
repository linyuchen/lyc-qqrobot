from sqlalchemy import Column, String, Integer

from src.db.models.base import Base


class Subscriber(Base):
    __tablename__ = "github_subscriber"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(String)
    platform = Column(String)
    owner = Column(String)
    repo = Column(String)
    event = Column(String)
    action = Column(String)