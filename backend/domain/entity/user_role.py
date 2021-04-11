from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from domain.base import Base


class UserRole(Base):
    __tablename__ = 'user_role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), name='user_id')
    role_id = Column(Integer, ForeignKey('role.id'), name='role_id')
    insert_date_time = Column(DateTime, name='created_datetime', default=datetime.now(), nullable=False)

    user = relationship("User")
    role = relationship("Role")