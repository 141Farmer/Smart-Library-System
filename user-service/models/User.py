from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from database.Base import Base
from typing import Optional
from enum import Enum as Enums

class UserRole(str, Enums):
    STUDENT = "student"
    FACULTY = "faculty"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    email = Column(String(30), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)  # Fixed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.utcnow)