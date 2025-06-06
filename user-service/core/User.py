from fastapi  import HTTPException, status
from schemas.User import RegisterAction, UserResponse, DetailedUserResponse, UpdateAction
from database.Session import session_instance
from typing  import List
from models.User import User as UserTable

class User:

    def register(self, register_info: RegisterAction) -> UserResponse:
        try:
            existing_user = session_instance.read_filter_one(UserTable, name=register_info.name)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this name already exists"
                )

            user = UserTable(
                name=register_info.name,
                email=register_info.email,
                role=register_info.role
            )
            session_instance.write(user)

            new_user = session_instance.read_filter_one(UserTable, name=register_info.name)
            if not new_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user"
                )

            return UserResponse(
                id=new_user.id,
                name=new_user.name,
                email=new_user.email,
                role=new_user.role,
                created_at=new_user.created_at
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Registration failed: {str(e)}"
            )

    def get_user(self, id: int) -> DetailedUserResponse:
        user = session_instance.read_one(UserTable, id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    
        return DetailedUserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    def update_user(self, id: int, update_info: UpdateAction) -> DetailedUserResponse:
        try:
            user = session_instance.update(UserTable, id, update_info)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return DetailedUserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Update failed: {str(e)}"
            )