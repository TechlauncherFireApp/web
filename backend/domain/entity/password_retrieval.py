from datetime import datetime
from domain.base import Base
from sqlalchemy import Column, String, DateTime, Integer

class PasswordRetrieval(Base):
    __tablename__ = 'password_verify'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256), name='email', unique=True)
    code = Column(String(256), name='code', nullable=False)
    created_datetime = Column(DateTime, name='created_datetime', default=datetime.now(), nullable=False)
    expired_datetime = Column(DateTime, name='expired_datetime', default=datetime.now(), nullable=False)
