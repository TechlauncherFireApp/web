import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from backend.domain.base import Base
from backend.domain.guid import GUID


class AssetRequestVehicle(Base):
    __tablename__ = 'asset-request-vehicle'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    request_id = Column(Integer, ForeignKey('asset-request.id'))
    type = Column(String, name='type')
    from_date_time = Column(DateTime, name='from')
    to_date_time = Column(DateTime, name='to')
    update_date_time = Column(DateTime, name='lastUpdateDt')
    insert_date_time = Column(DateTime, name='rowInsertDT')
