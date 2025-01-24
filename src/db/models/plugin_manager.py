from sqlalchemy.ext.mutable import MutableList

from src.db.models.base import Base
from sqlalchemy import Column, String, Boolean, JSON


class PluginManager(Base):
    __tablename__ = "plugin_manager"
    plugin_id = Column(String, primary_key=True)
    global_disable = Column(Boolean, default=False)
    disable_groups = Column(MutableList.as_mutable(JSON), default=lambda: [])
