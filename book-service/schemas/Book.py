from pydantic  import BaseModel
from datetime import  datetime

class AddBookAction(BaseModel):
    title: str
    author: str
    isbn: str
    copies: int

class DetailedBookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    copies: int
    available_copies: int
    created_at: datetime
    updated_at: datetime | None 

class UpdateBookAction(BaseModel):
    copies: int
    available_copies: int

class MiniBookResponse(BaseModel):
    id: int
    title: str
    author: str

class BookNumberAction(BaseModel):
    available_copies: int
    borrow_count: int