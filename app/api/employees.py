from app.db.connections import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends, APIRouter
from app.services.employee_service import create,view_one,view_all,update,view_me
from app.schemas.employee_schema import EmployeeCreate,EmployeeShow,EmployeeUpdate
from app.core.security import has_role,get_id

employee=APIRouter(prefix="/api/v1/employee")

@employee.post("/create",response_model=EmployeeShow)
def add_employee(request:EmployeeCreate,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return create(request,db)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@employee.get("/view_all_employee",response_model=list[EmployeeShow])
def show_all_employees(employee_id:int= Depends(get_id),db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr','manager']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_all(role,employee_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@employee.get("/view_one_employee/{employee_id}",response_model=EmployeeShow)
def show_one_employees(employee_id:int,db:Session = Depends(get_db),user_id:int=Depends(get_id),role:str = Depends(has_role(['admin','hr','manager']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_one(user_id,role,employee_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@employee.put("/update_employee/{employee_id}",response_model=EmployeeShow)
def change_employee(employee_id:int,request:EmployeeUpdate,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return update(employee_id,request,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@employee.get("/view_me",response_model=EmployeeShow)
def show_me(employee_id:int = Depends(get_id),db:Session = Depends(get_db)):
    try:
        if employee_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="No such Employee")
        return view_me(employee_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))




