import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.domain.base import Base
from backend.domain.guid import GUID


class AssetRequestVolunteer(Base):
    __tablename__ = 'asset-request_volunteer'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4().hex[0:15])
    volunteer_id = Column(GUID(), ForeignKey('volunteer.id'), name='idVolunteer')
    vehicle_id = Column(GUID(), ForeignKey('asset-request-vehicle.id'), name='idVehicle')
    position = Column(Integer, name='position')
    roles = Column(String, name='roles')
    status = Column(String, name='status')
    update_date_time = Column(DateTime, name='lastUpdateDt', default=datetime.now(), nullable=False)
    insert_date_time = Column(DateTime, name='rowInsertDT', default=datetime.now(), nullable=False)

    asset_request_vehicle = relationship("AssetRequestVehicle")
