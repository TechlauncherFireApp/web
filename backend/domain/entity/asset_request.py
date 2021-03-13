import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.domain.base import Base
from backend.domain.guid import GUID


class AssetRequest(Base):
    __tablename__ = 'asset-request'

    id = Column(GUID, primary_key=True, default=uuid.uuid4().hex[0:15])
    admin_id = Column(GUID, ForeignKey('admin.id'), name='idAdmin', nullable=False)
    title = Column(String, name='title', nullable=False)
    status = Column(String, name='status', default='waiting', nullable=False)
    update_date_time = Column(DateTime, name='lastUpdateDt', default=datetime.now(), nullable=False)
    insert_date_time = Column(DateTime, name='rowInsertDT', default=datetime.now(), nullable=False)

    asset_request_vehicle = relationship("AssetRequestVehicle")