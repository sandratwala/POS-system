from uuid import UUID

from app.models.receipt import Receipt
from sqlalchemy.orm import Session

class ReceiptRepository:
    def __init__(self):
        self.model=Receipt
        
    def get(self, db: Session, id: str):
        return db.get(Receipt, UUID(id))
    
    def get_all(self, db:Session):
        return db.query(Receipt).all()
    
    def get_all_by_type(self, db:Session, type:str):
        return db.query(Receipt).filter(Receipt.type == type).all()
    
    def create(self, db: Session, data:dict):
        receipt=Receipt(**data)
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        return receipt
    
    def update(self, db: Session, db_obj: Receipt, data:dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete (self, db: Session, db_obj:Receipt):
        db.delete(db_obj)
        db.commit()
        

receipt_repository=ReceiptRepository()