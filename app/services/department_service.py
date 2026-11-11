from fastapi import HTTPException,status
from app.models.department_model import Department
from app.schemas.department_schema import DepartmentCreate,DepartmentUpdate
from sqlalchemy.orm import Session
from app.repositories.department_repo import create_new_department,get_all_departments,existing_department,get_one_department,update_department,get_department_by_id

def create(request:DepartmentCreate,db:Session):
    try:
        check_department_exists=existing_department(request.department_name,db)
        if check_department_exists is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Department already exists")
        department=Department(department_name=request.department_name)
        return create_new_department(department,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def  view_all(db:Session):
    try:
        return get_all_departments(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def view_one(department_id:int,db:Session):
    try:
        department=get_one_department(department_id,db)
        if department is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Department not found")
        else:        
            return department
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))    

def update(department_id:int,request:DepartmentUpdate,db:Session):
    try:
        department=get_department_by_id(department_id,db)
        if department is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Department not found")
        if request.department_name is not None:
            department.department_name=request.department_name
        if request.is_active is not None:
            department.is_active=request.is_active
        return update_department(department,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

  