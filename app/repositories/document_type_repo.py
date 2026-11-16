from sqlalchemy.orm import Session
from app.models.document_type_model import DocumentType
from fastapi import HTTPException,status

def existing_document_type(document_type_name:str,db:Session):
    try:
        return db.query(DocumentType).filter(DocumentType.document_type_name.ilike(document_type_name)).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such document_type")

def create_new_document_type(document_type:DocumentType,db:Session):
    try:
        db.add(document_type)
        db.commit()
        db.refresh(document_type)
        return document_type
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_document_types(db:Session):
    try:
        return db.query(DocumentType.document_type_id,DocumentType.document_type_name,
                        DocumentType.description,DocumentType.requires_hr_approval,DocumentType.is_active).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_one_document_type(document_type_id:int,db:Session):
    try:
        return db.query(DocumentType.document_type_id,DocumentType.document_type_name,
                        DocumentType.description,DocumentType.requires_hr_approval,DocumentType.is_active).filter(
                        DocumentType.document_type_id==document_type_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_document_type_by_id(document_type_id:int,db:Session):
    try:
        return db.query(DocumentType).filter(DocumentType.document_type_id==document_type_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def update_document_type(document_type:DocumentType,db:Session):
    try:
        db.commit()
        db.refresh(document_type)
        return get_one_document_type(document_type.document_type_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

        
    




