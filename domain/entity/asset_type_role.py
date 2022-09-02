from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from domain.base import Base


class AssetTypeRole(Base):
    __tablename__ = 'asset_type_role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_type_id = Column(Integer, ForeignKey('asset_type.id'), name='asset_type_id')
    seat_number = Column(Integer, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), name='role_id')
    insert_date_time = Column(DateTime, name='created_datetime', default=datetime.now(), nullable=False)

    asset_type = relationship("AssetType")
    role = relationship("Role")