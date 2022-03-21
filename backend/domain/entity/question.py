from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, JSON
from domain.base import Base
from domain.type.question_type import QuestionType
from domain.type.difficulty_level import Difficulty


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_time = Column(DateTime, name='created_time', default=datetime.now(), nullable=False)
    updated_time = Column(DateTime, name='updated_time', default=datetime.now(), nullable=False)
    question_type = Column(Enum(QuestionType), name='question_type')
    role = Column(String(100), name='role')
    choices = Column(JSON, name='choices', default=None)
    description = Column(String(512), default=None)
    difficulty = Column(Enum(Difficulty, name='difficulty'))
    answer = Column(String(5), name='answer', nullable=False)
