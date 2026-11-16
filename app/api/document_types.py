from app.db.connections import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends, APIRouter
from app.services.document_type_service import create,view_one,view_all,update
from app.schemas.document_type_schema import DocumentTypeCreate,DocumentTypeUpdate,DocumentTypeShow
from app.core.security import has_role

document_type=APIRouter(prefix="/api/v1/document_type")

@document_type.post("/create",response_model=DocumentTypeShow)
def add_document_type(request:DocumentTypeCreate,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return create(request,db)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@document_type.get("/view_all_document_type",response_model=list[DocumentTypeShow])
def show_all_document_types(db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr','manager','employee']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_all(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@document_type.get("/view_one_document_type/{document_type_id}",response_model=DocumentTypeShow)
def show_one_document_types(document_type_id:int,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_one(document_type_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@document_type.put("/update_document_type/{document_type_id}",response_model=DocumentTypeShow)
def change_document_type(document_type_id:int,request:DocumentTypeUpdate,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return update(document_type_id,request,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


