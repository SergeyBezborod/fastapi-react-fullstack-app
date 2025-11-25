from sqlalchemy.sql import or_
from sqlalchemy.orm import Session
from ..models.user_models import UserBase
from ..schemas.user_schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> UserBase | None:
        return self.db.query(UserBase).filter(UserBase.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> UserBase | None:
        return self.db.query(UserBase).filter(UserBase.username == username).first()
    
    def get_user_by_email(self, email: str) -> UserBase | None:
        return self.db.query(UserBase).filter(UserBase.email == email).first()
    
    def get_user_by_username_or_email(self, username_or_email: str) -> UserBase:
        return self.db.query(UserBase).filter(or_(UserBase.username == username_or_email, UserBase.email == username_or_email)).first()
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> list[UserBase]:
        return self.db.query(UserBase).offset(skip).limit(limit).all()
    
    def get_active_users(self) -> list[UserBase]:
        return self.db.query(UserBase).filter(UserBase.is_active == True).all()

    def create_user(self, user_data: UserCreate) -> UserBase:
        db_user = UserBase(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            bio=user_data.bio,
            avatar_url=user_data.avatar_url
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user_data(self, user_id: int, user_data: UserUpdate) -> UserBase:
        db_user = self.get_user_by_id(user_id)
        if db_user:
            update_data = user_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_user, field, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user
    
    def update_user_password(self, user_id: int, new_password: str) -> UserBase:
        db_user = self.get_user_by_id(user_id)
        if db_user:
            db_user.password = new_password
            self.db.commit()
            self.db.refresh(db_user)
        return db_user
    
    def delete_user(self, user_id: int) -> UserBase:
        db_user = self.get_user_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user
    
    def deactivate_user(self, user_id: int) -> UserBase:
        db_user = self.get_user_by_id(user_id)
        if db_user:
            db_user.is_active = False
            self.db.commit()
            self.db.refresh(db_user)
        return db_user
    
    def set_online_status(self, user_id: int, is_online: bool) -> UserBase:
        db_user = self.get_user_by_id(user_id)
        if db_user:
            db_user.is_online = is_online
            self.db.commit()
            self.db.refresh(db_user)
        return db_user