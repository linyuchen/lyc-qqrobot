
from src.db.models.base import Base
from sqlalchemy import Column, String


class ChatModel(Base):
    """
    model 和 context_id 绑定，可以实现不同聊天对象使用不同的模型
    """
    __tablename__ = "ai_chat_models"
    context_id = Column(String, primary_key=True)
    model = Column(String)
