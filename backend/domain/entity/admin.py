import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from backend.domain.base import Base
from backend.domain.guid import GUID


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, name='firstName')
    last_name = Column(String, name='lastName')
    mobile_number = Column(String, name='mobileNo', unique=True)
    email = Column(String, name='email', unique=True)
    insert_date_time = Column(DateTime, name='rowInsertDT')

    asset_request = relationship("AssetRequest")