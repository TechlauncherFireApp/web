from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from backend.domain.base import Base


class AssetRequestVolunteer(Base):
    __table_name__ = 'asset-request_volunteer'

    id = Column(Integer, primary_kery=True, autoincrement=True)

    volunteer_id = Column(Integer, ForeignKey('volunteer.id'))
    vehicle_id = Column(Integer, ForeignKey('asset-request-vehicle.id'))
    position = Column(Integer, name='position')
    roles = Column(String, name='roles')
    status = Column(JSON, name='status')
    update_date_time = Column(DateTime, name='lastUpdateDt')
    insert_date_time = Column(DateTime, name='rowInsertDT')

    asset_request_vehicle = relationship("AssetRequestVehicle", back_populates="asset-request_volunteer")
    volunteer = relationship("AssetRequest", back_populates="asset-request_volunteer")