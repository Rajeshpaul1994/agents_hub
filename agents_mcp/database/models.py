from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base


class AgentUser(Base):

    __tablename__ = "agent_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    agent_uuid = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="agent", nullable=False)
    goal = Column(Text, nullable=True)


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    agent_id = Column(
        Integer,
        ForeignKey("agent_users.id"),
        nullable=False
    )
    created_at = Column(DateTime, server_default=func.now())

    agent = relationship("AgentUser")