from pydantic  import BaseModel

class RegisterAction(BaseModel):
    name: str
    email: str
    role: str

class UserResponse(BaseModel):
    name: str
    email: str
    role: str
    books_borrowed:  int
    current_borrows: int

class MiniUserResponse(BaseModel):
    id: int
    name: str
    email: str

class UserLoanAction(BaseModel):
    books_borrowed: int
    current_borrows: int