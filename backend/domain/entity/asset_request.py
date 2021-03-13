import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.domain.base import Base
from backend.domain.guid import GUID


class AssetRequest(Base):
    __tablename__ = 'asset-request'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    admin_id = Column(Integer, ForeignKey('admin.id'), name='idAdmin')
    title = Column(String, name='title')
    status = Column(String, name='status')
    update_date_time = Column(DateTime, name='lastUpdateDt')
    insert_date_time = Column(DateTime, name='rowInsertDT')

    asset_request_vehicle = relationship("AssetRequestVehicle")