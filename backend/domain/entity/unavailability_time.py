from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from datetime import datetime
from domain import Base


class UnavailabilityTime(Base):
    __tablename__ = 'unavailability_time'
    eventId = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    title = Column(String(256), nullable=True, default=None)
    periodicity = Column(Integer, nullable=False, default=1)
    start = Column(DateTime, nullable=False, default=datetime.now())
    end = Column(DateTime, nullable=False, default=datetime.now())
    status = Column(Boolean, nullable=False, default=1)
    UniqueConstraint(eventId, userId, name='event')
