from sqlalchemy import Column, Integer, String, DateTime,  Float
from database.Base import Base
from datetime import datetime
from typing import Optional


class Book(Base):
    __tablename__='books'
    id: int=Column(Integer, primary_key=True)
    title: str=Column(String, unique=True, nullable=False)
    author: str=Column(String, nullable=False)
    isbn: str=Column(String, unique=True, nullable=False)
    copies: int=Column(Integer, default=0)
    available_copies: int=Column(Integer, default=0)
    created_at: datetime=Column(DateTime, default=datetime.utcnow)
    updated_at: Optional[datetime]=Column(DateTime, default=None, onupdate=datetime.utcnow)
    borrow_count: int=Column(Integer, default=0)
    new_count: float=Column(Float, default=0.0)
    another_count:   float=Column(Float, default=0.1)
    no_count:   float=Column(Float, default=0.1)
    two_count:   float=Column(Float, default=0.1)