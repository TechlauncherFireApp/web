from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from domain.base import Base


class AssetRequest(Base):
    __tablename__ = 'asset_request'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), name='user_id', nullable=False)
    title = Column(String(256), name='title', nullable=False)
    status = Column(String(256), name='status', default='waiting', nullable=False)
    update_date_time = Column(DateTime, name='last_update_datetime', default=datetime.now(), nullable=False)
    insert_date_time = Column(DateTime, name='created_datetime', default=datetime.now(), nullable=False)

    user = relationship("User")