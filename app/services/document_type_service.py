from fastapi import HTTPException,status
from app.models.document_type_model import DocumentType
from app.schemas.document_type_schema import DocumentTypeCreate,DocumentTypeUpdate
from sqlalchemy.orm import Session
from app.repositories.document_type_repo import create_new_document_type,get_all_document_types,existing_document_type,get_one_document_type,update_document_type,get_document_type_by_id

def create(request:DocumentTypeCreate,db:Session):
    try:
        check_document_type_exists=existing_document_type(request.document_type_name,db)
        if check_document_type_exists is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="DocumentType already exists")
        document_type=DocumentType(document_type_name=request.document_type_name,
                             description=request.description,
                             requires_hr_approval=request.requires_hr_approval)
        return create_new_document_type(document_type,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def  view_all(db:Session):
    try:
        return get_all_document_types(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def view_one(document_type_id:int,db:Session):
    try:
        document_type=get_one_document_type(document_type_id,db)
        if document_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="DocumentType not found")
        else:        
            return document_type
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))    

def update(document_type_id:int,request:DocumentTypeUpdate,db:Session):
    try:
        document_type=get_document_type_by_id(document_type_id,db)
        if document_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="DocumentType not found")
        if request.document_type_name is not None:
            document_type.document_type_name=request.document_type_name
        if request.description is not None:
            document_type.description=request.description
        if request.requires_hr_approval is not None:
            document_type.requires_hr_approval=request.requires_hr_approval
        if request.is_active is not None:
            document_type.is_active=request.is_active
        return update_document_type(document_type,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

  