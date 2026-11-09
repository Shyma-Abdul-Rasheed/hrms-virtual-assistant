from sqlalchemy.orm import Session
from app.models.employee_model import Employee
from app.models.department_model import Department
from fastapi import HTTPException,status

def existing_employee(email:str,db:Session):
    try:
        return db.query(Employee).filter(Employee.email==email).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))
        
def create_new_employee(employee:Employee,db:Session):
    try:
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_employees(db:Session):
    try:
        return (
            db.query(
                Employee.employee_id,
                Employee.employee_code,
                Employee.full_name,
                Employee.email,
                Department.department_name,
                Employee.designation,
                Employee.role,
                Employee.is_active,
            )
            .join(Department,Department.department_id==Employee.department_id)
            .all()
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_dept_employees(employee_id:int,db:Session):
    try:
        dept_id=db.query(Employee.department_id).filter(Employee.employee_id==employee_id).scalar()
        if dept_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee or department not found")

        return (
            db.query(
                Employee.employee_id,
                Employee.employee_code,
                Employee.full_name,
                Employee.email,
                Department.department_name,
                Employee.designation,
                Employee.role,
                Employee.is_active,
            )
            .join(Department,Department.department_id==Employee.department_id)
            .filter(Employee.department_id==dept_id)
            .all()
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))


def get_one_employee(employee_id:int,db:Session):
    try:
        return (
                    db.query(
                        Employee.employee_id,
                        Employee.employee_code,
                        Employee.full_name,
                        Employee.email,
                        Department.department_name,
                        Employee.designation,
                        Employee.role,
                        Employee.is_active,
                    )
                    .join(Department,Department.department_id==Employee.department_id)
                    .filter(Employee.employee_id==employee_id)
                    .first()
                )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def update_employee(employee:Employee,db:Session):
    try:
        db.commit()
        db.refresh(employee)
        return get_one_employee(employee.employee_id,db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_employee_by_id(employee_id:int,db:Session):
    try:
        return db.query(Employee).filter(Employee.employee_id==employee_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))


        
    




