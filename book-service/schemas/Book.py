from pydantic  import BaseModel
from datetime import  datetime

class AddBookAction(BaseModel):
    title: str
    author: str
    isbn: str
    copies: int

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    copies: int
    available_copies: int
    created_at: datetime

class SearchBookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    copies: int
    available_copies: int

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
   
class BookAvailabiltyAction(BaseModel):
    available_copies: int
    operation: str

class BookAvailabiltyResponse(BaseModel):
    id: int
    available_copies: int
    updated_at: datetime

class AvailableCopyAction(BaseModel):
    available_copies: int