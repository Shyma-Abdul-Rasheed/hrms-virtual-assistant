from sqlalchemy.orm import Session
from app.models.leave_request_model import LeaveRequest
from app.models.leave_type_model import LeaveType
from app.models.employee_model import Employee
from app.models.department_model import Department
from fastapi import HTTPException,status
from datetime import date

def existing_leave_request(employee_id:int,start_date:date,end_date:date,db:Session,exclude_id:int |None=None):
    try:
        query=db.query(LeaveRequest).filter(LeaveRequest.employee_id==employee_id,LeaveRequest.start_date<=end_date,
                LeaveRequest.end_date>=start_date,LeaveRequest.status.in_(["pending", "approved"]))
        if exclude_id is not None:
            query=query.filter(LeaveRequest.leave_request_id!=exclude_id)
        return query.first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def create_new_leave_request(leave_request:LeaveRequest,db:Session):
    try:
        db.add(leave_request)
        db.commit()
        db.refresh(leave_request)
        return leave_request
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_requests(db:Session):
    try:
        return db.query(LeaveRequest.leave_request_id,Employee.employee_code,Employee.full_name,
                        Department.department_name,LeaveType.leave_type_name,LeaveRequest.start_date,
                        LeaveRequest.end_date,LeaveRequest.days_requested,
                        LeaveRequest.reason,LeaveRequest.status,LeaveRequest.created_at.label("submitted_at")).join(
                            Employee,Employee.employee_id==LeaveRequest.employee_id).join(
                                LeaveType,LeaveType.leave_type_id==LeaveRequest.leave_type_id).join(
                                    Department,Employee.department_id==Department.department_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_requests_by_manager(department_id:int,db:Session):
    try:
        return db.query(LeaveRequest.leave_request_id,Employee.employee_code,Employee.full_name,
                                Department.department_name,LeaveType.leave_type_name,LeaveRequest.start_date,
                                LeaveRequest.end_date,LeaveRequest.days_requested,
                                LeaveRequest.reason,LeaveRequest.status,LeaveRequest.created_at.label("submitted_at")).join(
                                    Employee,Employee.employee_id==LeaveRequest.employee_id).join(
                                        LeaveType,LeaveType.leave_type_id==LeaveRequest.leave_type_id).join(
                                            Department,Employee.department_id==Department.department_id).filter(
                                                Employee.department_id==department_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_one_leave_request(leave_request_id:int,db:Session):
    try:
        return db.query(LeaveRequest.leave_request_id,Employee.employee_code,Employee.full_name,
                                Department.department_name,LeaveType.leave_type_name,LeaveRequest.start_date,
                                LeaveRequest.end_date,LeaveRequest.days_requested,
                                LeaveRequest.reason,LeaveRequest.status,LeaveRequest.created_at.label("submitted_at")).join(
                                    Employee,Employee.employee_id==LeaveRequest.employee_id).join(
                                        LeaveType,LeaveType.leave_type_id==LeaveRequest.leave_type_id).join(
                                            Department,Employee.department_id==Department.department_id).filter(
                                                LeaveRequest.leave_request_id==leave_request_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_one_leave_request_by_manager(leave_request_id:int,department_id:int,db:Session):
    try:
        return db.query(LeaveRequest.leave_request_id,Employee.employee_code,Employee.full_name,
                                Department.department_name,LeaveType.leave_type_name,LeaveRequest.start_date,
                                LeaveRequest.end_date,LeaveRequest.days_requested,
                                LeaveRequest.reason,LeaveRequest.status,LeaveRequest.created_at.label("submitted_at")).join(
                                    Employee,Employee.employee_id==LeaveRequest.employee_id).join(
                                        LeaveType,LeaveType.leave_type_id==LeaveRequest.leave_type_id).join(
                                            Department,Employee.department_id==Department.department_id).filter(
                                                LeaveRequest.leave_request_id==leave_request_id,Employee.department_id==department_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_leave_request_by_id(leave_request_id:int,db:Session):
    try:
        return db.query(LeaveRequest).filter(LeaveRequest.leave_request_id==leave_request_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_leave_request_by_id_for_update(leave_request_id:int,db:Session):
    try:
        return db.query(LeaveRequest).filter(LeaveRequest.leave_request_id==leave_request_id).with_for_update().first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_request_of_employee(employee_id:int,db:Session):
    try:
            return db.query(LeaveRequest.leave_request_id,Employee.employee_code,Employee.full_name,
                                    Department.department_name,LeaveType.leave_type_name,LeaveRequest.start_date,
                                    LeaveRequest.end_date,LeaveRequest.days_requested,
                                    LeaveRequest.reason,LeaveRequest.status,LeaveRequest.created_at.label("submitted_at")).join(
                                        Employee,Employee.employee_id==LeaveRequest.employee_id).join(
                                            LeaveType,LeaveType.leave_type_id==LeaveRequest.leave_type_id).join(
                                                Department,Employee.department_id==Department.department_id).filter(
                                                    LeaveRequest.employee_id==employee_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_request_of_employee_by_manager(employee_id:int,department_id:int,db:Session):
    try:
            return db.query(LeaveRequest.leave_request_id,Employee.employee_code,Employee.full_name,
                                    Department.department_name,LeaveType.leave_type_name,LeaveRequest.start_date,
                                    LeaveRequest.end_date,LeaveRequest.days_requested,
                                    LeaveRequest.reason,LeaveRequest.status,LeaveRequest.created_at.label("submitted_at")).join(
                                        Employee,Employee.employee_id==LeaveRequest.employee_id).join(
                                            LeaveType,LeaveType.leave_type_id==LeaveRequest.leave_type_id).join(
                                                Department,Employee.department_id==Department.department_id).filter(
                                                    LeaveRequest.employee_id==employee_id,Employee.department_id==department_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def update_leave_request(leave_request:LeaveRequest,db:Session):
    try:
        db.commit()
        db.refresh(leave_request)
        return get_one_leave_request(leave_request.leave_request_id,db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

        
    




