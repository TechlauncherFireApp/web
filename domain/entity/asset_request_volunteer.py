from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from domain.base import Base


class AssetRequestVolunteer(Base):
    __tablename__ = 'asset_request_volunteer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), name='user_id')
    vehicle_id = Column(Integer, ForeignKey('asset_request_vehicle.id'), name='vehicle_id')
    role_id = Column(Integer, ForeignKey('role.id'), name='role_id')
    status = Column(String(256), name='status')
    update_date_time = Column(DateTime, name='last_update_datetime', default=datetime.now(), nullable=False)
    insert_date_time = Column(DateTime, name='created_datetime', default=datetime.now(), nullable=False)
    qualification_id = Column(Integer, ForeignKey('qualification.id'), name='qualification_id')

    asset_request_vehicle = relationship("AssetRequestVehicle")
    user = relationship("User")
    role = relationship("Role")
    qualification = relationship("Qualification")
