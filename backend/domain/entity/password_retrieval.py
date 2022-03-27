from datetime import datetime
from domain.base import Base
from sqlalchemy import Column, String, DateTime, Integer
class PasswordVerification(Base):
    __tablename__ = 'password_verify'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256), name='email', unique=True)
    code = Column(String(256), name='code', nullable=False)
    created_time = Column(DateTime, name='created_datetime', default=datetime.now(), nullable=False)
    expired_time = Column(DateTime, name='expired_datetime', default=datetime.now(), nullable=False)
