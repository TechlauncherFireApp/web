from sqlalchemy import Column, String, DateTime, Integer, Enum, JSON

from domain.base import Base
from domain.type import UserType


class TenancyType(Base):
    __tablename__ = 'tenancy_type'
    id = Column(Integer, primary_key=True, autoincrement=True)


