import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

from backend.domain.base import Base
from backend.domain.guid import GUID
from backend.domain.type import UserType


class User(Base):
    __tablename__ = 'user'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4().hex[0:15])
    role = Column(Enum(UserType), name='userType', nullable=False)
    admin_id = Column(GUID, ForeignKey('admin.id'), name='adminId', nullable=True)
    volunteer_id = Column(GUID, ForeignKey('volunteer.id'), name='volunteerId', nullable=True)
    password = Column(String, nullable=True)
    incorrect_password_count = Column(Integer, default=0, name='incorrectPasswordCount')
    last_sign_in = Column(DateTime, default=0, name='lastSignInDt')
    update_date_time = Column(DateTime, name='lastUpdateDt', default=datetime.now(), nullable=False)
    insert_date_time = Column(DateTime, name='rowInsertDT', default=datetime.now(), nullable=False)