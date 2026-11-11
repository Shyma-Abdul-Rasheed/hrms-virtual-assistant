from sqlalchemy.orm import Session
from app.models.department_model import Department
from fastapi import HTTPException,status

def existing_department(department_name:str,db:Session):
    try:
        return db.query(Department).filter(Department.department_name.ilike(department_name)).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such department")

def create_new_department(department:Department,db:Session):
    try:
        db.add(department)
        db.commit()
        db.refresh(department)
        return department
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_departments(db:Session):
    try:
        return db.query(Department.department_id,Department.department_name,Department.is_active).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_one_department(department_id:int,db:Session):
    try:
        return db.query(Department.department_id,Department.department_name,Department.is_active).filter(Department.department_id==department_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_department_by_id(department_id:int,db:Session):
    try:
        return db.query(Department).filter(Department.department_id==department_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def update_department(department:Department,db:Session):
    try:
        db.commit()
        db.refresh(department)
        return get_one_department(department.department_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

        
    




