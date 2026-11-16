from fastapi import HTTPException,status
from app.models.document_request_model import DocumentRequest
from app.schemas.document_request_schema import DocumentRequestCreate,DocumentRequestUpdate,DocumentRequestStatusUpdate
from sqlalchemy.orm import Session
from app.repositories.document_request_repo import (create_new_document_request,get_all_document_requests,existing_document_request,
get_one_document_request,update_document_request,get_document_request_by_id,get_document_request_of_employee)
from app.repositories.document_type_repo import existing_document_type
from app.repositories.employee_repo import get_employee_by_id

def create(request:DocumentRequestCreate,user_id,db:Session):
    try:
        document_type=existing_document_type(request.document_type_name,db)
        if document_type is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No such Document Type")
        if not document_type.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Document Type not available")
        check_document_request_exists=existing_document_request(document_type.document_type_id,user_id,db)
        if check_document_request_exists is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="DocumentRequest already exists")
        document_request=DocumentRequest(employee_id=user_id,
                            document_type_id=document_type.document_type_id,
                            purpose=request.purpose)
        new_document_request= create_new_document_request(document_request,db)
        return get_one_document_request(new_document_request.document_request_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def  view_all(db:Session):
    try:
        return get_all_document_requests(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def view_one(document_request_id:int,db:Session):
    try:
        document_request=get_one_document_request(document_request_id,db)
        if document_request is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="DocumentRequest not found")
        else:        
            return document_request
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))  

def view_employee(user_id:int,db:Session):
    try:
        document_request=get_document_request_of_employee(user_id,db)
        if document_request is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="DocumentRequest not found")
        return document_request
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))  

def update_request(document_request_id:int,request:DocumentRequestUpdate,user_id:int,db:Session):
    try:
        document_request=get_document_request_by_id(document_request_id,db)
        if document_request is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="DocumentRequest not found")
        employee=get_employee_by_id(document_request.employee_id,db)
        if employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
        if employee.employee_id!=user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You cannot update this request")
        if request.status is not None:
            if document_request.status!="pending":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You cannot update approved or rejected request")
            document_request.status=request.status
        if request.purpose is not None:
            document_request.purpose=request.purpose
        return update_document_request(document_request,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def update_status(document_request_id:int,request:DocumentRequestStatusUpdate,user_id:int,role:str,db:Session):
    try:
        document_request=get_document_request_by_id(document_request_id,db)
        if document_request is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="DocumentRequest not found")
        employee=get_employee_by_id(document_request.employee_id,db)
        if employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
        approver=get_employee_by_id(user_id,db)
        if approver is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
        if employee.employee_id==user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You cannot update this request")
        if role=="hr" and employee.role=="hr":
            if approver.designation !="HR Manager":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You cannot update this request")
        if request.status is not None:
            if document_request.status!="pending":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You cannot update approved or rejected request")
            document_request.status=request.status
        return update_document_request(document_request,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

  