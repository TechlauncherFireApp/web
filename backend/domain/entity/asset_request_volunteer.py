import uuid

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from backend.domain.base import Base
from backend.domain.guid import GUID


class AssetRequestVolunteer(Base):
    __tablename__ = 'asset-request_volunteer'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    volunteer_id = Column(Integer, ForeignKey('volunteer.id'))
    vehicle_id = Column(Integer, ForeignKey('asset-request-vehicle.id'))
    position = Column(Integer, name='position')
    roles = Column(String, name='roles')
    status = Column(JSON, name='status')
    update_date_time = Column(DateTime, name='lastUpdateDt')
    insert_date_time = Column(DateTime, name='rowInsertDT')

    asset_request_vehicle = relationship("AssetRequestVehicle")
