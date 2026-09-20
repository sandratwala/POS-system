from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.receipt import receipt_repository
from app.schemas.receipt import ReceiptCreate, ReceiptUpdate

def get_receipt(db: Session, receipt_id: str):
    receipt = receipt_repository.get(db, receipt_id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found"
        )
    return receipt

def list_receipts(db: Session):
    return receipt_repository.get_all(db)

def create_receipt(db: Session, data: ReceiptCreate):
    return receipt_repository.create(db, data.model_dump())

def update_receipt(db: Session, receipt_id: str, data: ReceiptUpdate):
    receipt = get_receipt(db, receipt_id)
    return receipt_repository.update(db, receipt, data.model_dump(exclude_unset=True))

def delete_receipt(db: Session, receipt_id: str):
    receipt = get_receipt(db, receipt_id)
    receipt_repository.delete(db, receipt)
