from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.payment import payment_repository
from app.schemas.payment import PaymentCreate, PaymentUpdate

def get_payment(db: Session, payment_id: str):
    payment = payment_repository.get(db, payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found"
        )
    return payment

def list_payments(db: Session):
    return payment_repository.get_all(db)

def list_payments_by_status(db: Session, payment_status: str):
    return payment_repository.get_all_by_status(db, payment_status)

def create_payment(db: Session, data: PaymentCreate):
    return payment_repository.create(db, data.model_dump())

def update_payment(db: Session, payment_id: str, data: PaymentUpdate):
    payment = get_payment(db, payment_id)
    return payment_repository.update(db, payment, data.model_dump(exclude_unset=True))

def delete_payment(db: Session, payment_id: str):
    payment = get_payment(db, payment_id)
    payment_repository.delete(db, payment)
