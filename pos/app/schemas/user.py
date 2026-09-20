from datetime import datetime
from app.models.user import UserRole
from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class UserBase(BaseModel):
    username: str
    password : str
    first_name : str
    last_name : str
    email: str
    role: UserRole
    is_active :Optional [bool] = None
    
class UserCreate(UserBase):
    password:str

class UserUpdate(BaseModel):
        password : Optional [str] =None
        name : Optional [str] =None
        last_name : Optional [str] =None
        email: Optional [str] =None
        role: Optional [UserRole] =None
        is_active: Optional [bool] = None
        
class UserRead(UserBase):
    model_config=ConfigDict(from_attributes=True)
    
    user_id: UUID
    is_active: bool 
    created_at: datetime
    updated_at : datetime
    