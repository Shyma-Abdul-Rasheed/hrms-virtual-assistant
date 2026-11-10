from fastapi import HTTPException,status
from app.models.employee_model import Employee
from app.schemas.employee_schema import EmployeeCreate,EmployeeUpdate
from sqlalchemy.orm import Session
from app.repositories.employee_repo import existing_employee,create_new_employee,update_employee,get_one_employee,get_all_employees,get_employee_by_id,get_dept_employees,get_one_employee_dept
from app.repositories.department_repo import existing_department

def create(request:EmployeeCreate,db:Session):
    try:
        check_employee_exists=existing_employee(request.email,db)
        if check_employee_exists is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Employee already exists")
        department=existing_department(request.department_name,db)
        if department is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such department")
        employee=Employee(full_name=request.full_name,
                          email=request.email,
                          department_id=department.department_id,
                          designation=request.designation,
                          role=request.role)
        new_employee= create_new_employee(employee,db)
        return get_one_employee(new_employee.employee_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def  view_all(role:str,employee_id:int,db:Session):
    try:
        if role=="manager":
            return get_dept_employees(employee_id,db)
        else:
            return get_all_employees(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def view_one(user_id:int,role:str,employee_id:int,db:Session):
    try:
        if role=="manager":
            employee=get_one_employee_dept(user_id,employee_id,db)
        else:
            employee=get_one_employee(employee_id,db)
        if employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
        else:        
            return employee
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))    

def update(employee_id:int,request:EmployeeUpdate,db:Session):
    try:
        check_employee=get_employee_by_id(employee_id,db)
        if check_employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
        if request.full_name is not None:
            check_employee.employee_name=request.employee_name
        if request.email is not None:
            check_employee.email=request.email
        if request.department_name is not None:
            check_department=existing_department(request.department_name,db)
            if check_department:
                check_employee.department_id=check_department.department_id
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such department")
        if request.designation is not None:
            check_employee.designation=request.designation
        if request.role is not None:
            check_employee.role=request.role
        if request.is_active is not None:
            check_employee.is_active=request.is_active
        return update_employee(check_employee,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def view_me(employee_id:int,db:Session):
    try:
        return get_one_employee(employee_id,db)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


  