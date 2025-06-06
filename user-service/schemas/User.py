from pydantic  import BaseModel
from datetime import  datetime

class RegisterAction(BaseModel):
    name: str
    email: str
    role: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

class DetailedUserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime
    updated_at: datetime | None

class UpdateAction(BaseModel):
    name: str
    email: str