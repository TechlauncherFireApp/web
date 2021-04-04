from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from domain.base import Base


class Qualifications(Base):
    __tablename__ = 'qualifications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)
    update_date_time = Column(DateTime, name='last_update_datetime', default=datetime.now(), nullable=False)
    insert_date_time = Column(DateTime, name='created_datetime', default=datetime.now(), nullable=False)
