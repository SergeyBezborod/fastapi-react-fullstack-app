from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from typing import List
from typing import List
from ..database import get_db
from ..schemas.user_schemas import (
    UserUpdatePassword, UserCreate, UserUpdate, 
    UserLogin, UserResponse, UserListResponse
)
from ..services.user_services import UserService, get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.register_user(user)

@router.post("/login", response_model=UserResponse)
async def login_user(user: UserLogin, user_service: UserService = Depends(get_user_service)):
    return user_service.authenticate_user(user)

@router.get("/all", response_model=List[UserListResponse])
async def get_all_users(skip: int = 0, limit: int = 100, user_service: UserService = Depends(get_user_service)):
    return user_service.get_all_users(skip, limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.get_user_by_id(user_id)

@router.put("/update-data/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, user_service: UserService = Depends(get_user_service)):
    return user_service.update_user(user_id, user_data)

@router.patch("/update-password/{user_id}")
async def update_user_password(user_id: int, password_data: UserUpdatePassword, user_service: UserService = Depends(get_user_service)):
    return user_service.update_user_password(user_id, password_data)

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.delete_user(user_id)

@router.post("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.deactivate_user(user_id)

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    # не реализовано
    # return user_service.get_current_user()
    ):
    return {"message": "Not implemented"}