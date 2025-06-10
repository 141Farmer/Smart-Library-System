from datetime import datetime
from pydantic import BaseModel
from  typing import List


class LoanAction(BaseModel):
    user_id:  int
    book_id:  int
    due_date: datetime

class LoanResponse(BaseModel):
    id: int
    user_id: int
    book_id:  int
    issue_date: datetime
    due_date: datetime
    status: str

class ReturnAction(BaseModel):
    loan_id: int

class ReturnResponse(BaseModel):
    id: int
    user_id: int
    book_id:  int
    issue_date: datetime
    due_date: datetime
    return_date: datetime | None
    status: str

class MiniBookResponse(BaseModel):
    id: int
    title: str
    author: str

class MiniUserResponse(BaseModel):
    id: int
    name: str
    email: str

class  LoanHistoryResponse(BaseModel):
    id:  int
    book: MiniBookResponse
    issue_date: datetime
    due_date: datetime
    return_date: datetime | None
    status: str

class UsersLoanHistoryResponse(BaseModel):
    loans: List[LoanHistoryResponse]
    total: int

class SpecificLoanResponse(BaseModel):
    id:  int
    user: MiniUserResponse
    book: MiniBookResponse
    issue_date: datetime
    due_date: datetime
    return_date: datetime | None
    status: str

class BookAvailabiltyAction(BaseModel):
    available_copies: int
    operation: str

class ReturnUpdateAction(BaseModel):
    status: str
    return_date: datetime | None