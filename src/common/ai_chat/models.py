
from src.common.db.sqlalchemy import Base, init_db
from sqlalchemy import Column, String


class ChatModel(Base):
    """
    model 和 context_id 绑定，可以实现不同聊天对象使用不同的模型
    """
    __tablename__ = "ai_chat_models"
    context_id = Column(String, primary_key=True)
    model = Column(String)


db_session = init_db()

def get_chat_model(context_id: str):
    model: ChatModel = db_session.query(ChatModel).filter(ChatModel.context_id == context_id).first()
    if model:
        return model.model