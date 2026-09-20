from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.supplier import supplier_repository
from app.schemas.supplier import SupplierCreate, SupplierUpdate
from app.models.supplier import Supplier
from uuid import UUID

def get_supplier(db: Session, supplier_id: str):
    supplier = supplier_repository.get(db, supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found"
        )
    return supplier

def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Supplier]:
    return supplier_repository.get_all(db)

def list_suppliers(db: Session):
    return supplier_repository.get_all(db)

def create_supplier(db: Session, data: SupplierCreate):
    return supplier_repository.create(db, data.model_dump())

def update_supplier(db: Session, supplier_id: str, data: SupplierUpdate):
    supplier = get_supplier(db, supplier_id)
    return supplier_repository.update(db, supplier, data.model_dump(exclude_unset=True))

def delete_supplier(db: Session, supplier_id: str):
    supplier = get_supplier(db, supplier_id)
    supplier_repository.delete(db, supplier)