from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# Create a DeclarativeMeta instance
Base = declarative_base()


# Define To Do class inheriting from Base
class ToDo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80))
    task = Column(String(256))
