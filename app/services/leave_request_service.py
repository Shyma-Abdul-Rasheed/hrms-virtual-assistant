from decimal import Decimal
from fastapi import HTTPException,status
from datetime import date, timedelta
from app.models.leave_request_model import LeaveRequest
from app.schemas.leave_request_schema import LeaveRequestCreate,LeaveRequestUpdate
from sqlalchemy.orm import Session
from app.repositories.leave_request_repo import (create_new_leave_request,existing_leave_request,get_all_leave_requests,get_all_leave_requests_by_manager,get_one_leave_request,
        get_leave_request_by_id,get_one_leave_request_by_manager,get_all_leave_request_of_employee,get_all_leave_request_of_employee_by_manager,update_leave_request)
from app.repositories.employee_repo import get_employee_by_id
from app.repositories.leave_type_repo import existing_leave_type,get_leave_type_by_id
from app.repositories.leave_balance_repo import get_leave_balance_of_employee_by_leave_type,restore_leave_balance

def create(request:LeaveRequestCreate,user_id:int,db:Session):
    try:
        if request.start_date>request.end_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Start date cannot be greater than end date")
        if request.is_half_day:
            if request.start_date!=request.end_date:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Half-day leave must be for a single date")
            days_requested=Decimal("0.5")
        else:
            days_requested=Decimal((request.end_date - request.start_date).days + 1)
        leave_type=existing_leave_type(request.leave_type_name,db)
        if leave_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Leave Type does not exist")
        minimum_date = date.today() + timedelta(days=leave_type.min_notice_days)
        if request.start_date < minimum_date:
            raise HTTPException(status_code=400,detail="Leave request does not meet the minimum notice period")
        leave_balance=get_leave_balance_of_employee_by_leave_type(user_id,leave_type.leave_type_id,request.start_date.year,db)
        if leave_balance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Leave Balance does not exist")
        if leave_balance.balance_days<days_requested:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have enough leaves")
        check_leave_request_exists=existing_leave_request(user_id,request.start_date,request.end_date,db)
        if check_leave_request_exists is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You already have a pending or approved leave request for these dates")
        leave_request=LeaveRequest(employee_id=user_id,
                             leave_type_id=leave_type.leave_type_id,
                             start_date=request.start_date,
                             end_date=request.end_date,
                             days_requested=days_requested,
                             reason=request.reason)
        new_leave_request=create_new_leave_request(leave_request,db)
        return get_one_leave_request(new_leave_request.leave_request_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def  view_all(user_id:int,role:str,db:Session):
    try:
        if role=='manager':
            employee=get_employee_by_id(user_id,db)
            leave_request=get_all_leave_requests_by_manager(employee.department_id,db)
        else:
            leave_request=get_all_leave_requests(db)
        return leave_request
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def view_one(leave_request_id:int,user_id:int,role:str,db:Session):
    try:
        if role=='manager':
            employee=get_employee_by_id(user_id,db)
            leave_request=get_one_leave_request_by_manager(leave_request_id,employee.department_id,db)
            if leave_request is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You cannot view this employee")        
        else:
            leave_request=get_one_leave_request(leave_request_id,db)
            if leave_request is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="LeaveRequest not found")        
        return leave_request
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e)) 

def view_all_leave_request_of_employee(employee_id,user_id:int,role:str,db:Session):
    try:
        if role=='manager':
            employee=get_employee_by_id(user_id,db)
            leave_request=get_all_leave_request_of_employee_by_manager(employee_id,employee.department_id,db)
            if not leave_request:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You cannot view this employee")
        else:
            leave_request=get_all_leave_request_of_employee(employee_id,db)
            if not leave_request:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee or leave balances not found")
        return leave_request
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def view_me(employee_id:int,db:Session):
    try:
        return get_all_leave_request_of_employee(employee_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def update(leave_request_id:int,user_id:int,request:LeaveRequestUpdate,db:Session):
    try:
        leave_request=get_leave_request_by_id(leave_request_id,db)
        if leave_request is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Leave Request not found")
        if leave_request.employee_id!=user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You cannot update this leave request")
        #Handling cancellation
        if request.status=="cancelled":
            if leave_request.status not in ["pending","approved"]:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You cannot cancel this leave request")
            # If already approved, restore the deducted leave balance.
            if leave_request.status=="approved":
                # Cancellation must happen before the leave start date
                if date.today() >= leave_request.start_date:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Approved leave can only be cancelled before its start date")
                leave_balance=get_leave_balance_of_employee_by_leave_type(user_id,leave_request.leave_type_id,leave_request.start_date.year,db)
                if leave_balance is None:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Leave balance not found")
                if leave_balance.used_days < leave_request.days_requested:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You do not have enough leaves")
                restore_leave_balance(user_id,leave_request.leave_type_id,leave_request.start_date.year,leave_request.days_requested,db)
            leave_request.status = "cancelled"
            return update_leave_request(leave_request,db)
        # Only pending requests can have their details edited
        if leave_request.status!="pending":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Only pending requests can have their details edited")
        new_start_date = ( request.start_date if request.start_date is not None else leave_request.start_date)
        new_end_date = ( request.end_date if request.end_date is not None else leave_request.end_date)
        if new_start_date>new_end_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Start date cannot be greater than end date")
        if request.is_half_day:
            if new_start_date!=new_end_date:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Half-day leave must be for a single date")
            new_days_requested=Decimal("0.5")
        else:
            new_days_requested=Decimal((new_end_date- new_start_date).days + 1)
        leave_type=get_leave_type_by_id(leave_request.leave_type_id,db)
        if leave_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Leave Type does not exist")
        if new_start_date != leave_request.start_date:
            minimum_date = date.today() + timedelta(days=leave_type.min_notice_days)
            if new_start_date < minimum_date:
                raise HTTPException(status_code=400,detail="Leave request does not meet the minimum notice period")
        leave_balance=get_leave_balance_of_employee_by_leave_type(user_id,leave_request.leave_type_id,new_start_date.year,db)
        if leave_balance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Leave Balance does not exist")
        if leave_balance.balance_days<new_days_requested:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have enough leaves")
        check_leave_request_exists=existing_leave_request(user_id,new_start_date,new_end_date,db,exclude_id=leave_request_id)
        if check_leave_request_exists is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You already have a pending or approved leave request for these dates")
        leave_request.start_date = new_start_date
        leave_request.end_date = new_end_date
        leave_request.days_requested = new_days_requested
        if request.reason is not None:
            leave_request.reason=request.reason
        return update_leave_request(leave_request, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

  