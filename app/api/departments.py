from app.db.connections import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends, APIRouter
from app.services.department_service import create,view_one,view_all,update
from app.schemas.department_schema import DepartmentCreate,DepartmentUpdate,DepartmentShow
from app.core.security import has_role

department=APIRouter(prefix="/api/v1/department")

@department.post("/create",response_model=DepartmentShow)
def add_department(request:DepartmentCreate,db:Session = Depends(get_db),role:str = Depends(has_role(['admin']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return create(request,db)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@department.get("/view_all_department",response_model=list[DepartmentShow])
def show_all_departments(db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_all(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@department.get("/view_one_department/{department_id}",response_model=DepartmentShow)
def show_one_departments(department_id:int,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_one(department_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@department.put("/update_department/{department_id}",response_model=DepartmentShow)
def change_department(department_id:int,request:DepartmentUpdate,db:Session = Depends(get_db),role:str = Depends(has_role(['admin']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return update(department_id,request,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


