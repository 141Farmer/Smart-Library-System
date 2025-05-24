from fastapi import APIRouter
from core.User import User
from schemas.User import RegisterAction, UserResponse

router=APIRouter(prefix='',tags=['User'])

user=User()

@router.post("/users/")
def register(registerInfo: RegisterAction):
    return user.register(registerInfo)

@router.get("/users/{id}",  response_model=UserResponse)
def getUser(id):
    return user.getUser(id)