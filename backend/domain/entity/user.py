from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, Enum, JSON
from sqlalchemy.orm import relationship

from backend.domain.base import Base
from backend.domain.type import UserType


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(Enum(UserType), name='user_type', nullable=False)
    password = Column(String(256), nullable=True)
    incorrect_password_count = Column(Integer, default=0, name='incorrect_password_count')
    last_sign_in = Column(DateTime, default=0, name='last_sign_in_datetime')
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    mobile_number = Column(String(256), name='mobile_number', unique=True)
    email = Column(String(256), name='email', unique=True)
    preferred_hours = Column(Integer, name='preferred_hours')
    experience_years = Column(Integer, name='experience_years')
    possibleRoles = Column(JSON, name='possible_roles')
    qualifications = Column(JSON, name='qualifications')
    availabilities = Column(JSON, name='availabilities')
    update_date_time = Column(DateTime, name='last_update_datetime', default=datetime.now(), nullable=False)
    insert_date_time = Column(DateTime, name='created_datetime', default=datetime.now(), nullable=False)

    asset_request = relationship("AssetRequest")
    asset_request_volunteer = relationship("AssetRequestVolunteer")
