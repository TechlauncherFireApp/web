from sqlalchemy import Column, Integer, String, DateTime

from backend.domain.base import Base


class Admin(Base):
    __table_name__ = 'admin'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, name='firstName')
    last_name = Column(String, name='lastName')
    mobile_number = Column(String, name='mobileNo', unique=True)
    email = Column(String, name='email', unique=True)
    insert_date_time = Column(DateTime, name='rowInsertDT')
