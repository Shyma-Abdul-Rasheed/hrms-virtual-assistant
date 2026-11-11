from app.db.connections import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends, APIRouter
from app.services.leave_type_service import create,view_one,view_all,update
from app.schemas.leave_type_schema import LeaveTypeCreate,LeaveTypeUpdate,LeaveTypeShow
from app.core.security import has_role

leave_type=APIRouter(prefix="/api/v1/leave_type")

@leave_type.post("/create",response_model=LeaveTypeShow)
def add_leave_type(request:LeaveTypeCreate,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return create(request,db)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_type.get("/view_all_leave_type",response_model=list[LeaveTypeShow])
def show_all_leave_types(db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr','manager','employee']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_all(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_type.get("/view_one_leave_type/{leave_type_id}",response_model=LeaveTypeShow)
def show_one_leave_types(leave_type_id:int,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr','manager','employee']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_one(leave_type_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_type.put("/update_leave_type/{leave_type_id}",response_model=LeaveTypeShow)
def change_leave_type(leave_type_id:int,request:LeaveTypeUpdate,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return update(leave_type_id,request,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


