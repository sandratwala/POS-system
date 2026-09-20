import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.schemas.payment import PaymentUpdate, PaymentCreate, PaymentRead
from app.services import payment as payment_service

router = APIRouter(prefix="/payment", tags=["Payment"])


@router.get("/", response_model=list[PaymentRead])
def list_payments(db: Session = Depends(get_db)):
    return payment_service.list_payments(db)


@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    return payment_service.get_payment(db, payment_id)


@router.get("/status/{payment_status}", response_model=list[PaymentRead])
def list_payments_by_status(payment_status: str, db: Session = Depends(get_db)):
    return payment_service.list_payments_by_status(db, payment_status)


@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    return payment_service.create_payment(db, data)


@router.put("/{payment_id}", response_model=PaymentRead)
def update_payment(
    payment_id: str, data: PaymentUpdate, db: Session = Depends(get_db)
):
    if hasattr(data, "sale_id") and isinstance(data.sale_id, str):
        data.sale_id = uuid.UUID(data.sale_id)

    return payment_service.update_payment(db, payment_id, data)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: str, db: Session = Depends(get_db)):
    return payment_service.delete_payment(db, payment_id)
