from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.orm import Session

from database import get_db
from app.schemas.user import UserCreate
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register(db, data)


@router.post("/login")
def login(username: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    token = auth_service.authenticate(db, username, password)
    return token
