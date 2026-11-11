from fastapi import HTTPException,status
from app.models.leave_type_model import LeaveType
from app.schemas.leave_type_schema import LeaveTypeCreate,LeaveTypeUpdate
from sqlalchemy.orm import Session
from app.repositories.leave_type_repo import create_new_leave_type,get_all_leave_types,existing_leave_type,get_one_leave_type,update_leave_type,get_leave_type_by_id

def create(request:LeaveTypeCreate,db:Session):
    try:
        check_leave_type_exists=existing_leave_type(request.leave_type_name,db)
        if check_leave_type_exists is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="LeaveType already exists")
        if request.min_notice_days<0:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Notice Days cannot be a negative number")
        leave_type=LeaveType(leave_type_name=request.leave_type_name,
                             description=request.description,
                             is_paid=request.is_paid,
                             min_notice_days=request.min_notice_days)
        return create_new_leave_type(leave_type,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def  view_all(db:Session):
    try:
        return get_all_leave_types(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def view_one(leave_type_id:int,db:Session):
    try:
        leave_type=get_one_leave_type(leave_type_id,db)
        if leave_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="LeaveType not found")
        else:        
            return leave_type
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))    

def update(leave_type_id:int,request:LeaveTypeUpdate,db:Session):
    try:
        leave_type=get_leave_type_by_id(leave_type_id,db)
        if leave_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="LeaveType not found")
        if request.leave_type_name is not None:
            leave_type.leave_type_name=request.leave_type_name
        if request.description is not None:
            leave_type.description=request.description
        if request.is_paid is not None:
            leave_type.is_paid=request.is_paid
        if request.min_notice_days is not None:
            if request.min_notice_days<0:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Notice Days cannot be a negative number")
            leave_type.min_notice_days=request.min_notice_days
        return update_leave_type(leave_type,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

  