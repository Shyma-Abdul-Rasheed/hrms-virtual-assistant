from app.db.connections import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends, APIRouter
from app.services.leave_approval_service import create
from app.schemas.leave_approval_schema import LeaveApprovalCreate,LeaveApprovalShow
from app.core.security import has_role,get_id

leave_approval=APIRouter(prefix="/api/v1/leave_approval")

@leave_approval.post("/create",response_model=LeaveApprovalShow)
def add_leave_request(request:LeaveApprovalCreate,db:Session = Depends(get_db),user_id:int=Depends(get_id),role:str = Depends(has_role(['hr','manager','admin']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return create(request,user_id,role,db)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))