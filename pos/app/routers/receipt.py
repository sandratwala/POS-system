import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.schemas.receipt import ReceiptUpdate, ReceiptCreate, ReceiptRead
from app.services import receipt as receipt_service

router = APIRouter(prefix="/receipt", tags=["Receipt"])


@router.get("/", response_model=list[ReceiptRead])
def list_receipts(db: Session = Depends(get_db)):
    return receipt_service.list_receipts(db)


@router.get("/{receipt_id}", response_model=ReceiptRead)
def get_receipt(receipt_id: str, db: Session = Depends(get_db)):
    return receipt_service.get_receipt(db, receipt_id)


@router.post("/", response_model=ReceiptRead, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=ReceiptRead, status_code=status.HTTP_201_CREATED)
def create_receipt(data: ReceiptCreate, db: Session = Depends(get_db)):
    return receipt_service.create_receipt(db, data)


@router.put("/{receipt_id}", response_model=ReceiptRead)
def update_receipt(
    receipt_id: str, data: ReceiptUpdate, db: Session = Depends(get_db)
):
    if hasattr(data, "sale_id") and isinstance(data.sale_id, str):
        data.sale_id = uuid.UUID(data.sale_id)

    return receipt_service.update_receipt(db, receipt_id, data)


@router.delete("/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt(receipt_id: str, db: Session = Depends(get_db)):
    return receipt_service.delete_receipt(db, receipt_id)
