from app.db.connections import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends, APIRouter
from app.services.leave_request_service import create,view_one,view_all,update,view_all_leave_request_of_employee,view_me
from app.schemas.leave_request_schema import LeaveRequestCreate,LeaveRequestUpdate,LeaveRequestShow
from app.core.security import has_role,get_id

leave_request=APIRouter(prefix="/api/v1/leave_request")

@leave_request.post("/create",response_model=LeaveRequestShow)
def add_leave_request(request:LeaveRequestCreate,db:Session = Depends(get_db),user_id:int=Depends(get_id),role:str = Depends(has_role(['hr','manager','employee']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return create(request,user_id,db)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_request.get("/view_all_leave_request",response_model=list[LeaveRequestShow])
def show_all_leave_requests(db:Session = Depends(get_db),user_id:int=Depends(get_id),role:str = Depends(has_role(['admin','hr','manager']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_all(user_id,role,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_request.get("/view_one_leave_request/{leave_request_id}",response_model=LeaveRequestShow)
def show_one_leave_requests(leave_request_id:int,user_id:int=Depends(get_id),db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr','manager']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_one(leave_request_id,user_id,role,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_request.get("/view_one_employee_leave_request/{employee_id}",response_model=list[LeaveRequestShow])
def show_employee_leave_requests(employee_id:int,db:Session = Depends(get_db),user_id:int=Depends(get_id),role:str = Depends(has_role(['admin','hr','manager']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_all_leave_request_of_employee(employee_id,user_id,role,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_request.get("/view_my_leave_request",response_model=list[LeaveRequestShow])
def show_one_leave_requests(employee_id:int = Depends(get_id),db:Session = Depends(get_db)):
    try:
        if employee_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="No such employee")
        return view_me(employee_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_request.put("/update_leave_request/{leave_request_id}",response_model=LeaveRequestShow)
def change_leave_request(leave_request_id:int,request:LeaveRequestUpdate,user_id:int=Depends(get_id),db:Session = Depends(get_db),role:str = Depends(has_role(['hr','manager','employee']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return update(leave_request_id,user_id,request,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


