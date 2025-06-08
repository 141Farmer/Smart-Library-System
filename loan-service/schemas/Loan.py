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

class LoanOfUserResponse(BaseModel):
    id: int
    book: MiniBookResponse
    issue_date: datetime
    due_date: datetime
    return_date: datetime | None
    status: str

class OverdueResponse(BaseModel):
    id: int
    user: MiniUserResponse
    book: MiniBookResponse
    issue_date: datetime
    due_date: datetime
    days_overdue: int

class ExtendLoanAction(BaseModel):
    extension_days: int

class UpdateLoanAction(BaseModel):
    extension_days: int
    extensions_count: int
    extended_due_date: datetime

class ExtendedLoanResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    issue_date: datetime
    original_due_date: datetime
    extended_due_date: datetime | None
    status: str
    extensions_count: int

class LoanIdAction(BaseModel):
    loan_id: int

class ReturnUpdateAction(BaseModel):
    status: str
    return_date: datetime | None

class UserLoanAction(BaseModel):
    books_borrowed: int
    current_borrows: int