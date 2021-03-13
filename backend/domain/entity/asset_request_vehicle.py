from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.domain.base import Base


class AssetRequestVehicle(Base):
    __table_name__ = 'asset-request-vehicle'

    id = Column(Integer, primary_kery=True, autoincrement=True)
    request_id = Column(Integer, ForeignKey('asset-request.id'))
    type = Column(String, name='type')
    from_date_time = Column(DateTime, name='from')
    to_date_time = Column(DateTime, name='to')
    update_date_time = Column(DateTime, name='lastUpdateDt')
    insert_date_time = Column(DateTime, name='rowInsertDT')

    asset_request = relationship("AssetRequest", back_populates="asset-request-vehicle")