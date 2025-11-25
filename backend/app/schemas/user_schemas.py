from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
from typing import Optional, Any
from datetime import datetime


#Request schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=25)
    email: EmailStr = Field(...)
    full_name: Optional[str] = Field(None)
    bio: Optional[str] = Field(None, max_length=1000)
    avatar_url: Optional[str] = Field(None)

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(..., min_length=10, max_length=128)
    
    @field_validator("username")
    @classmethod
    def deny_special_characters(cls, v):
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password_length(cls, v):
        if len(v.encode('utf-8')) > 128:
            raise ValueError("Password is too long (maximum 128 bytes)")
        return v


class UserLogin(BaseModel):
    username: str = Field(..., min_length=5, max_length=25)
    password: str = Field(..., min_length=10, max_length=128)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None)
    full_name: Optional[str] = Field(None)
    bio: Optional[str] = Field(None, max_length=1000)
    avatar_url: Optional[str] = Field(None)
    

class UserUpdatePassword(BaseModel):
    current_password: str = Field(..., min_length=10, max_length=128)
    new_password: str = Field(..., min_length=10, max_length=128)
    confirm_password: str = Field(..., min_length=10, max_length=128)

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info: Any) -> str:
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError("Passwords do not match")
        return v

    @field_validator("new_password")
    @classmethod
    def deny_same_password(cls, v: str, info: Any):
        if 'current_password' in info.data and v == info.data['current_password']:
            raise ValueError("New password cannot be the same as current password")
        return v
    
    @field_validator("current_password", "new_password", "confirm_password")
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        if len(v.encode('utf-8')) > 128:
            raise ValueError("Password is too long (maximum 128 bytes)")
        return v
    


#Response schemas
class UserResponse(UserBase):
    id: int = Field(...)
    is_active: bool = Field(...)
    is_online: bool = Field(...)
    last_seen: datetime = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)


class UserListResponse(BaseModel):
    id: int
    username: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    is_online: bool
    last_seen: datetime

    model_config = ConfigDict(from_attributes=True)