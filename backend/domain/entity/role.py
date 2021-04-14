from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from domain.base import Base


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(256), nullable=False)
    name = Column(String(256), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)
    update_date_time = Column(DateTime, name='last_update_datetime', default=datetime.now(), nullable=False)
    insert_date_time = Column(DateTime, name='created_datetime', default=datetime.now(), nullable=False)
