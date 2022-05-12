import sqlalchemy

from domain.base import Base
from sqlalchemy import *
from datetime import datetime


class ChatbotInput(Base):
    __tablename__ = 'chatbot_input'
    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_time = Column(sqlalchemy.DateTime, default=datetime.now(), nullable=False)
    user_email = Column(sqlalchemy.String(255), nullable=False)
    content = Column(sqlalchemy.TEXT)
