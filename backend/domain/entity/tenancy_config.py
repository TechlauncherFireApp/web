from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Boolean, BLOB, Text

from domain.base import Base


class TenancyConfig(Base):
    __tablename__ = 'tenancy_config'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    title = Column(String(256), nullable=False)
    font = Column(String(256), nullable=True)
    logo = Column(Text, nullable=False)
    logo_name = Column(Text, nullable=False)
    logo_mimetype = Column(Text, nullable=False)
    navbar_colour = Column(String(256), nullable=False)
    background_colour = Column(String(256), nullable=False)
    deleted = Column(Boolean, nullable=False, default=True)
    update_date_time = Column(DateTime, name='last_update_datetime', default=datetime.now(), nullable=False)
    insert_date_time = Column(DateTime, name='created_datetime', default=datetime.now(), nullable=False)
