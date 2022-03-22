from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text
from sqlalchemy.dialects.mysql import TINYINT
from domain.base import Base
from domain.type import QuestionType


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_time = Column(DateTime, default=datetime.now(), nullable=False)
    update_time = Column(DateTime, default=datetime.now(), nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    role = Column(String(256), nullable=True)
    description = Column(String(1024), nullable=False)
    choice = Column(Text, nullable=False)
    difficulty = Column(TINYINT, default=1, nullable=False)
    answer = Column(String(20), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    answered_time = Column(Integer, default=0, nullable=False)
    correct_time = Column(Integer, default=0, nullable=False)
