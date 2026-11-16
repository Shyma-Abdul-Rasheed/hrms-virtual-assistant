from app.db.connections import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends, APIRouter
from app.services.document_request_service import create,view_one,view_all,view_employee,update_request,update_status
from app.schemas.document_request_schema import DocumentRequestCreate,DocumentRequestUpdate,DocumentRequestStatusUpdate,DocumentRequestShow
from app.core.security import has_role,get_id

document_request=APIRouter(prefix="/api/v1/document_request")

@document_request.post("/create",response_model=DocumentRequestShow)
def add_document_request(request:DocumentRequestCreate,user_id:int=Depends(get_id),db:Session = Depends(get_db),role:str = Depends(has_role(['employee','manager','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return create(request,user_id,db)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@document_request.get("/view_all_document_request",response_model=list[DocumentRequestShow])
def show_all_document_requests(db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_all(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@document_request.get("/view_one_document_request/{document_request_id}",response_model=DocumentRequestShow)
def show_one_document_requests(document_request_id:int,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_one(document_request_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@document_request.get("/view_employee_document_request/{employee_id}",response_model=list[DocumentRequestShow])
def show_document_requests_employee(employee_id:int,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_employee(employee_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@document_request.get("/view_my_document_request",response_model=list[DocumentRequestShow])
def show_document_requests_employee(user_id:int=Depends(get_id),db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_employee(user_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@document_request.put("/update_document_request/{document_request_id}",response_model=DocumentRequestShow)
def change_document_request(document_request_id:int,request:DocumentRequestUpdate,user_id:int=Depends(get_id),db:Session = Depends(get_db),role:str = Depends(has_role(['employee','manager','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return update_request(document_request_id,request,user_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@document_request.put("/update_document_request_status/{document_request_id}",response_model=DocumentRequestShow)
def change_document_request_status(document_request_id:int,request:DocumentRequestStatusUpdate,user_id:int=Depends(get_id),db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return update_status(document_request_id,request,user_id,role,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


