from fastapi import HTTPException,status
from app.models.leave_balance_model import LeaveBalance
from app.schemas.leave_balance_schema import LeaveBalanceCreate,LeaveBalanceUpdate
from sqlalchemy.orm import Session
from app.repositories.leave_balance_repo import (create_new_leave_balance,get_all_leave_balances,existing_leave_balance,get_one_leave_balance,update_leave_balance,get_leave_balance_by_id,
get_all_leave_balance_of_employee,get_all_leave_balances_by_manager,get_one_leave_balance_by_manager,get_all_leave_balance_of_employee_by_manager)
from app.repositories.employee_repo import get_employee_by_id,get_employee_by_code
from app.repositories.leave_type_repo import existing_leave_type

def create(request:LeaveBalanceCreate,role:str,db:Session):
    try:
        employee=get_employee_by_code(request.employee_code,db)
        if employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
        if role=="hr" and employee.role=="hr":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="HR is not authorized to create another HR's leave balance")
        check_leave_balance_exists=existing_leave_balance(request.employee_code,request.leave_type_name,request.year,db)
        if check_leave_balance_exists is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Already created")
        if request.entitlement_days<0 or request.used_days<0:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Entitlement Days or Used Days cannot be a negative number")
        if request.entitlement_days<request.used_days:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Entitlement Days should be greater than used days")
        leave_type=existing_leave_type(request.leave_type_name,db)
        if leave_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Leave Type not found")
        leave_balance=LeaveBalance(employee_id=employee.employee_id,
                             leave_type_id=leave_type.leave_type_id,
                             year=request.year,
                             entitlement_days=request.entitlement_days,
                             used_days=request.used_days)
        new_leave_balance=create_new_leave_balance(leave_balance,db)
        return get_one_leave_balance(new_leave_balance.leave_balance_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def  view_all(user_id:int,role:str,db:Session):
    try:
        if role=='manager':
            employee=get_employee_by_id(user_id,db)
            leave_balance=get_all_leave_balances_by_manager(employee.department_id,db)
        else:
            leave_balance=get_all_leave_balances(db)
        return leave_balance
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def view_one(leave_balance_id:int,user_id:int,role:str,db:Session):
    try:
        if role=='manager':
            employee=get_employee_by_id(user_id,db)
            leave_balance=get_one_leave_balance_by_manager(leave_balance_id,employee.department_id,db)
            if leave_balance is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You cannot view this employee")        
        else:
            leave_balance=get_one_leave_balance(leave_balance_id,db)
            if leave_balance is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="LeaveBalance not found")        
        return leave_balance
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e)) 

def view_all_leave_balance_of_employee(employee_id,user_id:int,role:str,db:Session):
    try:
        if role=='manager':
            employee=get_employee_by_id(user_id,db)
            leave_balance=get_all_leave_balance_of_employee_by_manager(employee_id,employee.department_id,db)
            if not leave_balance:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You cannot view this employee")
        else:
            leave_balance=get_all_leave_balance_of_employee(employee_id,db)
            if not leave_balance:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee or leave balances not found")
        return leave_balance
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def view_me(employee_id:int,db:Session):
    try:
        return get_all_leave_balance_of_employee(employee_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def update(leave_balance_id:int,request:LeaveBalanceUpdate,role:str,db:Session):
    try:
        leave_balance=get_leave_balance_by_id(leave_balance_id,db)
        if leave_balance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="LeaveBalance not found")
        employee=get_employee_by_id(leave_balance.employee_id,db)
        if role=="hr" and employee.role=="hr":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="HR is not authorized to update another HR's leave balance")        
        
        if request.entitlement_days is not None:
            if request.entitlement_days<0:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Entitlement Days cannot be a negative number")
            leave_balance.entitlement_days=request.entitlement_days
        if request.used_days is not None:
            if request.used_days<0:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Used Days cannot be a negative number")
            leave_balance.used_days=request.used_days
        if leave_balance.entitlement_days<leave_balance.used_days:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Entitlement Days should be greater than used days")
        return update_leave_balance(leave_balance,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

  