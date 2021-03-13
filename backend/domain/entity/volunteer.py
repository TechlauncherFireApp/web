from sqlalchemy import Column, Integer, String, DateTime, JSON

from backend.domain.base import Base


class Volunteer(Base):
    __table_name__ = 'volunteer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, name='firstName')
    last_name = Column(String, name='lastName')
    mobile_number = Column(String, name='mobileNo', unique=True)
    email = Column(String, name='email', unique=True)
    preferred_hours = Column(Integer, name='prefHours')
    experience_years = Column(Integer, name='expYears')
    possibleRoles = Column(JSON, name='possibleRoles')
    qualifications = Column(JSON, name='qualifications')
    availabilities = Column(JSON, name='availabilities')
    update_date_time = Column(DateTime, name='lastUpdateDt')
    insert_date_time = Column(DateTime, name='rowInsertDT')
