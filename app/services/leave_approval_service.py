from decimal import Decimal
from fastapi import HTTPException,status
from datetime import date, timedelta
from app.models.leave_approval_model import LeaveApproval
from app.schemas.leave_approval_schema import LeaveApprovalCreate
from sqlalchemy.orm import Session
from app.repositories.leave_approval_repo import (create_new_leave_approval,get_all_leave_approvals,get_all_leave_approvals_by_manager,get_one_leave_approval,
        get_leave_approval_by_id,get_one_leave_approval_by_manager,get_all_leave_approval_of_employee,get_all_leave_approval_of_employee_by_manager,existing_leave_approval)
from app.repositories.employee_repo import get_employee_by_id
from app.repositories.leave_balance_repo import get_leave_balance_for_update
from app.repositories.leave_request_repo import get_leave_request_by_id_for_update

def create(request:LeaveApprovalCreate,user_id:int,role:str,db:Session):
    try:
        leave_approval=existing_leave_approval(request.leave_request_id,db)
        if leave_approval is not None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You have already decided on this leave request")
        leave_request=get_leave_request_by_id_for_update(request.leave_request_id,db)
        if leave_request is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such leave requests")
        if leave_request.status != "pending":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Only pending leave requests can be processed")
        approver=get_employee_by_id(user_id,db)
        if approver is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You cannot approve to this leave request")
        employee=get_employee_by_id(leave_request.employee_id,db)
        if employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such employee")
        if approver.employee_id==employee.employee_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You cannot approve to this leave request")
        if role=="hr" and employee.role=="hr":
            if approver.designation !="HR Manager":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You cannot approve this leave request")
        if role=="manager":
            if approver.department_id != employee.department_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You cannot approve this leave request")
        if request.decision=="approved":
            leave_balance=get_leave_balance_for_update(leave_request.employee_id,leave_request.leave_type_id,leave_request.start_date.year,db)
            if leave_balance is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Nos such leave balance for this employee")
            leave_balance.used_days+=leave_request.days_requested
        leave_request.status=request.decision
        leave_approval=LeaveApproval(approver_id=user_id,
                             leave_request_id=request.leave_request_id,
                             decision=request.decision,
                             comments=request.comments)
        new_leave_approval=create_new_leave_approval(leave_approval,db)
        return get_one_leave_approval(new_leave_approval.leave_approval_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

# def  view_all(user_id:int,role:str,db:Session):
#     try:
#         if role=='manager':
#             employee=get_employee_by_id(user_id,db)
#             leave_approval=get_all_leave_approvals_by_manager(employee.department_id,db)
#         else:
#             leave_approval=get_all_leave_approvals(db)
#         return leave_approval
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

# def view_one(leave_approval_id:int,user_id:int,role:str,db:Session):
#     try:
#         if role=='manager':
#             employee=get_employee_by_id(user_id,db)
#             leave_approval=get_one_leave_approval_by_manager(leave_approval_id,employee.department_id,db)
#             if leave_approval is None:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You cannot view this employee")        
#         else:
#             leave_approval=get_one_leave_approval(leave_approval_id,db)
#             if leave_approval is None:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="LeaveApproval not found")        
#         return leave_approval
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e)) 

# def view_all_leave_approval_of_employee(employee_id,user_id:int,role:str,db:Session):
#     try:
#         if role=='manager':
#             employee=get_employee_by_id(user_id,db)
#             leave_approval=get_all_leave_approval_of_employee_by_manager(employee_id,employee.department_id,db)
#             if not leave_approval:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You cannot view this employee")
#         else:
#             leave_approval=get_all_leave_approval_of_employee(employee_id,db)
#             if not leave_approval:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee or leave balances not found")
#         return leave_approval
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

# def view_me(employee_id:int,db:Session):
#     try:
#         return get_all_leave_approval_of_employee(employee_id,db)
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


  