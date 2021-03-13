import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from backend.domain.base import Base
from backend.domain.guid import GUID


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4().hex[0:15])
    first_name = Column(String, name='firstName', nullable=False)
    last_name = Column(String, name='lastName', nullable=False)
    mobile_number = Column(String, name='mobileNo', unique=True, nullable=False)
    email = Column(String, name='email', unique=True, nullable=False)
    insert_date_time = Column(DateTime, name='rowInsertDT', nullable=False)

    asset_request = relationship("AssetRequest")