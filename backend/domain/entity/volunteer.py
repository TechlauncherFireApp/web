import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship

from backend.domain.base import Base
from backend.domain.guid import GUID


class Volunteer(Base):
    __tablename__ = 'volunteer'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4().hex[0:15])
    first_name = Column(String, name='firstName')
    last_name = Column(String, name='lastName')
    mobile_number = Column(String, name='mobileNo', unique=True)
    email = Column(String, name='email', unique=True)
    preferred_hours = Column(Integer, name='prefHours')
    experience_years = Column(Integer, name='expYears')
    possibleRoles = Column(JSON, name='possibleRoles')
    qualifications = Column(JSON, name='qualifications')
    availabilities = Column(JSON, name='availabilities')
    update_date_time = Column(DateTime, name='lastUpdateDt', default=datetime.now(), nullable=False)
    insert_date_time = Column(DateTime, name='rowInsertDT', default=datetime.now(), nullable=False)

    asset_request_volunteer = relationship("AssetRequestVolunteer")