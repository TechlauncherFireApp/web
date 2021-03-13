from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.domain.base import Base


class AssetRequest(Base):
    __table_name__ = 'asset-request'

    id = Column(Integer, primary_kery=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey('admin.id'))
    title = Column(String, name='title')
    status = Column(String, name='status')
    update_date_time = Column(DateTime, name='lastUpdateDt')
    insert_date_time = Column(DateTime, name='rowInsertDT')

    admin = relationship("Admin", back_populates="asset-request")
