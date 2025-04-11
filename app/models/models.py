from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="tasks")

