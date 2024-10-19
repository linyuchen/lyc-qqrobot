from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.common import DB_PATH

Base = declarative_base()

engine = create_engine(f'sqlite:///{DB_PATH}')


def init_db():
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    return session
