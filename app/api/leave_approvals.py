from app.db.connections import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends, APIRouter
from app.services.leave_approval_service import create,view_one,view_all,view_all_leave_approval_of_employee
from app.schemas.leave_approval_schema import LeaveApprovalCreate,LeaveApprovalShow
from app.core.security import has_role,get_id

leave_approval=APIRouter(prefix="/api/v1/leave_approval")

@leave_approval.post("/create",response_model=LeaveApprovalShow)
def add_leave_approval(request:LeaveApprovalCreate,db:Session = Depends(get_db),user_id:int=Depends(get_id),role:str = Depends(has_role(['hr','manager','admin']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return create(request,user_id,role,db)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_approval.get("/view_all_leave_approval",response_model=list[LeaveApprovalShow])
def show_all_leave_approvals(db:Session = Depends(get_db),user_id:int=Depends(get_id),role:str = Depends(has_role(['admin','hr','manager']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_all(user_id,role,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_approval.get("/view_one_leave_approval/{leave_approval_id}",response_model=LeaveApprovalShow)
def show_one_leave_approvals(leave_approval_id:int,user_id:int=Depends(get_id),db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr','manager']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_one(leave_approval_id,user_id,role,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_approval.get("/view_one_employee_leave_approval/{employee_id}",response_model=list[LeaveApprovalShow])
def show_employee_leave_approvals(employee_id:int,db:Session = Depends(get_db),user_id:int=Depends(get_id),role:str = Depends(has_role(['admin','hr','manager']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_all_leave_approval_of_employee(employee_id,user_id,role,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
