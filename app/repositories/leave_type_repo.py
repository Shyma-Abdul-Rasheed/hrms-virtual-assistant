from sqlalchemy.orm import Session
from app.models.leave_type_model import LeaveType
from fastapi import HTTPException,status

def existing_leave_type(leave_type_name:str,db:Session):
    try:
        return db.query(LeaveType).filter(LeaveType.leave_type_name.ilike(leave_type_name)).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such leave_type")

def create_new_leave_type(leave_type:LeaveType,db:Session):
    try:
        db.add(leave_type)
        db.commit()
        db.refresh(leave_type)
        return leave_type
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_types(db:Session):
    try:
        return db.query(LeaveType.leave_type_id,LeaveType.leave_type_name,LeaveType.description,
        LeaveType.is_paid,LeaveType.min_notice_days).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_one_leave_type(leave_type_id:int,db:Session):
    try:
        return db.query(LeaveType.leave_type_id,LeaveType.leave_type_name,LeaveType.description,
        LeaveType.is_paid,LeaveType.min_notice_days).filter(LeaveType.leave_type_id==leave_type_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_leave_type_by_id(leave_type_id:int,db:Session):
    try:
        return db.query(LeaveType).filter(LeaveType.leave_type_id==leave_type_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def update_leave_type(leave_type:LeaveType,db:Session):
    try:
        db.commit()
        db.refresh(leave_type)
        return get_one_leave_type(leave_type.leave_type_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

        
    




