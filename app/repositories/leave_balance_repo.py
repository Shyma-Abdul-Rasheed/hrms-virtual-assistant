from decimal import Decimal

from sqlalchemy.orm import Session
from app.models.leave_balance_model import LeaveBalance
from app.models.employee_model import Employee
from app.models.department_model import Department
from app.models.leave_type_model import LeaveType
from fastapi import HTTPException,status

def existing_leave_balance(employee_code:str,leave_type_name:str,year:int,db:Session):
    try:
        return db.query(LeaveBalance).join(
            Employee,LeaveBalance.employee_id==Employee.employee_id).join(
                LeaveType,LeaveType.leave_type_id==LeaveBalance.leave_type_id).filter(
                    Employee.employee_code==employee_code,LeaveType.leave_type_name.ilike(leave_type_name),LeaveBalance.year==year).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such leave_balance")

def create_new_leave_balance(leave_balance:LeaveBalance,db:Session):
    try:
        db.add(leave_balance)
        db.commit()
        db.refresh(leave_balance)
        return leave_balance
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_balances(db:Session):
    try:
        return db.query(LeaveBalance.leave_balance_id,Employee.employee_code,Employee.full_name,
                        Department.department_name,LeaveType.leave_type_name,LeaveBalance.year,
                        LeaveBalance.entitlement_days,LeaveBalance.used_days,LeaveBalance.balance_days).join(
                            Employee,Employee.employee_id==LeaveBalance.employee_id).join(
                                LeaveType,LeaveType.leave_type_id==LeaveBalance.leave_type_id).join(
                                    Department,Department.department_id==Employee.department_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_one_leave_balance(leave_balance_id:int,db:Session):
    try:
        return db.query(LeaveBalance.leave_balance_id,Employee.employee_code,Employee.full_name,
                                Department.department_name,LeaveType.leave_type_name,LeaveBalance.year,
                                LeaveBalance.entitlement_days,LeaveBalance.used_days,LeaveBalance.balance_days).join(
                                    Employee,Employee.employee_id==LeaveBalance.employee_id).join(
                                        LeaveType,LeaveType.leave_type_id==LeaveBalance.leave_type_id).join(
                                            Department,Department.department_id==Employee.department_id).filter(
                                                LeaveBalance.leave_balance_id==leave_balance_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_balance_of_employee(employee_id:int,db:Session):
    try:
        return db.query(LeaveBalance.leave_balance_id,Employee.employee_code,Employee.full_name,
                                        Department.department_name,LeaveType.leave_type_name,LeaveBalance.year,
                                        LeaveBalance.entitlement_days,LeaveBalance.used_days,LeaveBalance.balance_days).join(
                                            Employee,Employee.employee_id==LeaveBalance.employee_id).join(
                                                LeaveType,LeaveType.leave_type_id==LeaveBalance.leave_type_id).join(
                                                    Department,Department.department_id==Employee.department_id).filter(
                                                        Employee.employee_id==employee_id).all()
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_leave_balance_by_id(leave_balance_id:int,db:Session):
    try:
        return db.query(LeaveBalance).filter(LeaveBalance.leave_balance_id==leave_balance_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_leave_balance_for_update(employee_id:int,leave_type_id:int,year:int,db:Session):
    try:
        return db.query(LeaveBalance).filter(LeaveBalance.employee_id==employee_id,
             LeaveBalance.leave_type_id==leave_type_id,LeaveBalance.year==year).with_for_update().first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def update_leave_balance(leave_balance:LeaveBalance,db:Session):
    try:
        db.commit()
        db.refresh(leave_balance)
        return get_one_leave_balance(leave_balance.leave_balance_id,db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_balances_by_manager(department_id:int,db:Session):
    try:
        return db.query(LeaveBalance.leave_balance_id,Employee.employee_code,Employee.full_name,
                                                Department.department_name,LeaveType.leave_type_name,LeaveBalance.year,
                                                LeaveBalance.entitlement_days,LeaveBalance.used_days,LeaveBalance.balance_days).join(
                                                    Employee,Employee.employee_id==LeaveBalance.employee_id).join(
                                                        LeaveType,LeaveType.leave_type_id==LeaveBalance.leave_type_id).join(
                                                            Department,Department.department_id==Employee.department_id).filter(
                                                                Employee.department_id==department_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_one_leave_balance_by_manager(leave_balance_id:int,department_id:int,db:Session):
    try:
            return db.query(LeaveBalance.leave_balance_id,Employee.employee_code,Employee.full_name,
                                    Department.department_name,LeaveType.leave_type_name,LeaveBalance.year,
                                    LeaveBalance.entitlement_days,LeaveBalance.used_days,LeaveBalance.balance_days).join(
                                        Employee,Employee.employee_id==LeaveBalance.employee_id).join(
                                            LeaveType,LeaveType.leave_type_id==LeaveBalance.leave_type_id).join(
                                                Department,Department.department_id==Employee.department_id).filter(
                                                    LeaveBalance.leave_balance_id==leave_balance_id,Employee.department_id==department_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_balance_of_employee_by_manager(employee_id:int,department_id:int,db:Session):
    try:
            return db.query(LeaveBalance.leave_balance_id,Employee.employee_code,Employee.full_name,
                                            Department.department_name,LeaveType.leave_type_name,LeaveBalance.year,
                                            LeaveBalance.entitlement_days,LeaveBalance.used_days,LeaveBalance.balance_days).join(
                                                Employee,Employee.employee_id==LeaveBalance.employee_id).join(
                                                    LeaveType,LeaveType.leave_type_id==LeaveBalance.leave_type_id).join(
                                                        Department,Department.department_id==Employee.department_id).filter(
                                                            Employee.employee_id==employee_id,Employee.department_id==department_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_leave_balance_of_employee_by_leave_type(employee_id:int,leave_type_id:int,year:int,db:Session):
    try:
        return db.query(LeaveBalance).filter(LeaveBalance.employee_id==employee_id,LeaveBalance.leave_type_id==leave_type_id,
                                             LeaveBalance.year==year).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def restore_leave_balance(employee_id:int,leave_type_id:int,year:int,days_requested:Decimal,db:Session):
    try:
        leave_balance = db.query(LeaveBalance).filter(LeaveBalance.employee_id == employee_id,
            LeaveBalance.leave_type_id == leave_type_id,LeaveBalance.year == year
            ).with_for_update().first()
        if leave_balance is not None:
            leave_balance.used_days -= days_requested
            db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))




        
    




