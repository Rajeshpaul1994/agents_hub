from sqlalchemy import Column, Integer, String, Text
from database.connection import Base


class AgentUser(Base):

    __tablename__ = "agent_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    agent_uuid = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="agent", nullable=False)
    goal = Column(Text, nullable=True)