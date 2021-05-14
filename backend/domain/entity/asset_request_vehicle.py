from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from domain.base import Base


class AssetRequestVehicle(Base):
    __tablename__ = 'asset_request_vehicle'

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(Integer, ForeignKey('asset_request.id'), name='request_id')
    asset_type_id = Column(Integer, ForeignKey('asset_type.id'), name='asset_type_id')
    from_date_time = Column(DateTime, name='from')
    to_date_time = Column(DateTime, name='to')
    update_date_time = Column(DateTime, name='last_update_datetime', default=datetime.now(), nullable=False)
    insert_date_time = Column(DateTime, name='created_datetime', default=datetime.now(), nullable=False)

    asset_request = relationship("AssetRequest")
    asset_type = relationship("AssetType")


