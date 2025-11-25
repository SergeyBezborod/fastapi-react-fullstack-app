from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from ..repositories.user_repositories import UserRepository
from ..schemas.user_schemas import (
    UserUpdatePassword, UserCreate, UserUpdate, 
    UserLogin, UserResponse, UserListResponse
    )


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
    
    def authenticate_user(self, login_data: UserLogin) -> UserResponse:
        db_user = self.user_repo.get_user_by_username_or_email(login_data.username)
        
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        if not db_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user",
            )

        if (db_user.password != login_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        
        return UserResponse.model_validate(db_user)
    
    def register_user(self, user_data: UserCreate) -> UserResponse:
        db_user = self.user_repo.get_user_by_username(user_data.username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists",
            )
        if self.user_repo.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )
        db_user = self.user_repo.create_user(user_data)
        return UserResponse.model_validate(db_user)
    
    def get_user_by_id(self, user_id: int) -> UserResponse:
        db_user = self.user_repo.get_user_by_id(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse.model_validate(db_user)
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> list[UserListResponse]:
        users = self.user_repo.get_all_users(skip, limit)
        return [UserListResponse.model_validate(user) for user in users]
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        if user_data.email:
            existing_user = self.user_repo.get_user_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )
        db_user = self.user_repo.update_user_data(user_id, user_data)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse.model_validate(db_user)
    
    def update_user_password(self, user_id: int, password_data: UserUpdatePassword) -> dict:
        db_user = self.user_repo.get_user_by_id(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if (db_user.password != password_data.current_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect current password",
            )
        new_password = password_data.new_password
        self.user_repo.update_user_password(user_id, new_password)

        return {"message": "Password updated successfully"}
    
    def delete_user(self, user_id: int) -> dict:
        if not self.user_repo.delete_user(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return {"message": "User deleted successfully"}
    
    def deactivate_user(self, user_id: int) -> UserResponse:
        db_user = self.user_repo.deactivate_user(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse.model_validate(db_user)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)