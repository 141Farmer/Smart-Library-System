from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from typing import Optional
from database.Base import Base

class Loan(Base):
    __tablename__='loans'
    id: int=Column(Integer, primary_key=True)
    user_id: int=Column(Integer, nullable=False)
    book_id: int=Column(Integer, nullable=False)
    original_due_date: datetime=Column(DateTime, nullable=False)
    issue_date: datetime=Column(DateTime, default=datetime.utcnow)
    return_date: Optional[datetime]=Column(DateTime, default=None)
    status: str=Column(String(10), default="ACTIVE")
    extension_count: int=Column(Integer, default=0)
    extended_due_date: Optional[datetime]=Column(DateTime, default=None)