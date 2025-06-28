from fastapi import APIRouter
from core.User import User
from schemas.User import RegisterAction, UserResponse, DetailedUserResponse, UpdateAction

router=APIRouter(prefix='/api',tags=['User'])

user=User()

@router.post("/users/", response_model=UserResponse)
def register(register_info: RegisterAction):
    return user.register(register_info)

@router.get("/users/{id}", response_model=DetailedUserResponse)
def get_user(id):
    return user.get_user(id)

@router.put("/users/{id}", response_model=DetailedUserResponse)
def update_user(id, update_info: UpdateAction):
    return user.update_user(id, update_info)