from sqlalchemy.orm import Session
from app.models.document_request_model import DocumentRequest
from app.models.document_type_model import DocumentType
from app.models.employee_model import Employee
from app.models.department_model import Department
from fastapi import HTTPException,status

def existing_document_request(document_type_id:int,employee_id:int,db:Session):
    try:
        return db.query(DocumentRequest).filter(DocumentRequest.document_type_id==document_type_id,
                DocumentRequest.employee_id==employee_id,DocumentRequest.status=="pending").first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such document_request")

def create_new_document_request(document_request:DocumentRequest,db:Session):
    try:
        db.add(document_request)
        db.commit()
        db.refresh(document_request)
        return document_request
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_document_requests(db:Session):
    try:
        return db.query(DocumentRequest.document_request_id,Employee.employee_code,
                        Employee.full_name,Employee.designation,Department.department_name,
                        DocumentType.document_type_name,DocumentRequest.purpose,
                        DocumentRequest.status).join(
                        DocumentType,DocumentRequest.document_type_id==DocumentType.document_type_id).join(
                        Employee,Employee.employee_id==DocumentRequest.employee_id).join(
                        Department,Department.department_id==Employee.department_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_one_document_request(document_request_id:int,db:Session):
    try:
        return db.query(DocumentRequest.document_request_id,Employee.employee_code,
                        Employee.full_name,Employee.designation,Department.department_name,
                        DocumentType.document_type_name,DocumentRequest.purpose,
                        DocumentRequest.status).join(
                        DocumentType,DocumentRequest.document_type_id==DocumentType.document_type_id).join(
                        Employee,Employee.employee_id==DocumentRequest.employee_id).join(
                        Department,Department.department_id==Employee.department_id).filter(
                        DocumentRequest.document_request_id==document_request_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_document_request_by_id(document_request_id:int,db:Session):
    try:
        return db.query(DocumentRequest).filter(DocumentRequest.document_request_id==document_request_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_document_request_of_employee(employee_id:int,db:Session):
    try:
        return db.query(DocumentRequest.document_request_id,Employee.employee_code,
                        Employee.full_name,Employee.designation,Department.department_name,
                        DocumentType.document_type_name,DocumentRequest.purpose,
                        DocumentRequest.status).join(
                        DocumentType,DocumentRequest.document_type_id==DocumentType.document_type_id).join(
                        Employee,Employee.employee_id==DocumentRequest.employee_id).join(
                        Department,Department.department_id==Employee.department_id).filter(
                        DocumentRequest.employee_id==employee_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def update_document_request(document_request:DocumentRequest,db:Session):
    try:
        db.commit()
        db.refresh(document_request)
        return get_one_document_request(document_request.document_request_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

        
    




