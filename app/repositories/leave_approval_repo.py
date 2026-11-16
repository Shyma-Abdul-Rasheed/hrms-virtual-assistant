from sqlalchemy.orm import Session,aliased
from app.models.leave_approval_model import LeaveApproval
from app.models.leave_type_model import LeaveType
from app.models.employee_model import Employee
from app.models.department_model import Department
from app.models.leave_request_model import LeaveRequest
from fastapi import HTTPException,status

def get_leave_approval_by_id(leave_approval_id:int,db:Session):
    try:
        return db.query(LeaveApproval).filter(LeaveApproval.leave_approval_id==leave_approval_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def existing_leave_approval(leave_request_id:int,db:Session):
    try:
        return db.query(LeaveApproval).filter(LeaveApproval.leave_request_id==leave_request_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def create_new_leave_approval(leave_approval:LeaveApproval,db:Session):
    try:
        db.add(leave_approval)
        db.commit()
        db.refresh(leave_approval)
        return leave_approval
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_approvals(db:Session):
    try:
        Approver=aliased(Employee)
        return db.query(LeaveApproval.leave_approval_id,Employee.employee_code,Employee.full_name,
                            Department.department_name,LeaveType.leave_type_name,LeaveRequest.start_date,
                            LeaveRequest.end_date,LeaveRequest.days_requested,
                            LeaveRequest.reason,LeaveApproval.decision,LeaveApproval.comments,
                            Approver.full_name.label("approved_by"),Approver.designation,LeaveApproval.approved_at).join(
                            LeaveRequest,LeaveRequest.leave_request_id==LeaveApproval.leave_request_id).join(
                            Employee,Employee.employee_id==LeaveRequest.employee_id).join(
                            Approver,Approver.employee_id==LeaveApproval.approver_id).join(
                            LeaveType,LeaveType.leave_type_id==LeaveRequest.leave_type_id).join(
                            Department,Employee.department_id==Department.department_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_approvals_by_manager(department_id:int,db:Session):
    try:
        Approver=aliased(Employee)
        return db.query(LeaveApproval.leave_approval_id,Employee.employee_code,Employee.full_name,
                            Department.department_name,LeaveType.leave_type_name,LeaveRequest.start_date,
                            LeaveRequest.end_date,LeaveRequest.days_requested,
                            LeaveRequest.reason,LeaveApproval.decision,LeaveApproval.comments,
                            Approver.full_name.label("approved_by"),Approver.designation,LeaveApproval.approved_at).join(
                            LeaveRequest,LeaveRequest.leave_request_id==LeaveApproval.leave_request_id).join(
                            Employee,Employee.employee_id==LeaveRequest.employee_id).join(
                            Approver,Approver.employee_id==LeaveApproval.approver_id).join(
                            LeaveType,LeaveType.leave_type_id==LeaveRequest.leave_type_id).join(
                            Department,Employee.department_id==Department.department_id).filter(
                        Employee.department_id==department_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_one_leave_approval(leave_approval_id:int,db:Session):
    try:
        Approver=aliased(Employee)
        return db.query(LeaveApproval.leave_approval_id,Employee.employee_code,Employee.full_name,
                            Department.department_name,LeaveType.leave_type_name,LeaveRequest.start_date,
                            LeaveRequest.end_date,LeaveRequest.days_requested,
                            LeaveRequest.reason,LeaveApproval.decision,LeaveApproval.comments,
                            Approver.full_name.label("approved_by"),Approver.designation,LeaveApproval.approved_at).join(
                            LeaveRequest,LeaveRequest.leave_request_id==LeaveApproval.leave_request_id).join(
                            Employee,Employee.employee_id==LeaveRequest.employee_id).join(
                            Approver,Approver.employee_id==LeaveApproval.approver_id).join(
                            LeaveType,LeaveType.leave_type_id==LeaveRequest.leave_type_id).join(
                            Department,Employee.department_id==Department.department_id).filter(
                            LeaveApproval.leave_approval_id==leave_approval_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_one_leave_approval_by_manager(leave_approval_id:int,department_id:int,db:Session):
    try:
        Approver=aliased(Employee)
        return db.query(LeaveApproval.leave_approval_id,Employee.employee_code,Employee.full_name,
                            Department.department_name,LeaveType.leave_type_name,LeaveRequest.start_date,
                            LeaveRequest.end_date,LeaveRequest.days_requested,
                            LeaveRequest.reason,LeaveApproval.decision,LeaveApproval.comments,
                            Approver.full_name.label("approved_by"),Approver.designation,LeaveApproval.approved_at).join(
                            LeaveRequest,LeaveRequest.leave_request_id==LeaveApproval.leave_request_id).join(
                            Employee,Employee.employee_id==LeaveRequest.employee_id).join(
                            Approver,Approver.employee_id==LeaveApproval.approver_id).join(
                            LeaveType,LeaveType.leave_type_id==LeaveRequest.leave_type_id).join(
                            Department,Employee.department_id==Department.department_id).filter(
                        LeaveApproval.leave_approval_id==leave_approval_id,Employee.department_id==department_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_approval_of_employee(employee_id:int,db:Session):
    try:
        Approver=aliased(Employee)
        return db.query(LeaveApproval.leave_approval_id,Employee.employee_code,Employee.full_name,
                            Department.department_name,LeaveType.leave_type_name,LeaveRequest.start_date,
                            LeaveRequest.end_date,LeaveRequest.days_requested,
                            LeaveRequest.reason,LeaveApproval.decision,LeaveApproval.comments,
                            Approver.full_name.label("approved_by"),Approver.designation,LeaveApproval.approved_at).join(
                            LeaveRequest,LeaveRequest.leave_request_id==LeaveApproval.leave_request_id).join(
                            Employee,Employee.employee_id==LeaveRequest.employee_id).join(
                            Approver,Approver.employee_id==LeaveApproval.approver_id).join(
                            LeaveType,LeaveType.leave_type_id==LeaveRequest.leave_type_id).join(
                            Department,Employee.department_id==Department.department_id).filter(
                        LeaveRequest.employee_id==employee_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def get_all_leave_approval_of_employee_by_manager(employee_id:int,department_id:int,db:Session):
    try:
        Approver=aliased(Employee)
        return db.query(LeaveApproval.leave_approval_id,Employee.employee_code,Employee.full_name,
                            Department.department_name,LeaveType.leave_type_name,LeaveRequest.start_date,
                            LeaveRequest.end_date,LeaveRequest.days_requested,
                            LeaveRequest.reason,LeaveApproval.decision,LeaveApproval.comments,
                            Approver.full_name.label("approved_by"),Approver.designation,LeaveApproval.approved_at).join(
                            LeaveRequest,LeaveRequest.leave_request_id==LeaveApproval.leave_request_id).join(
                            Employee,Employee.employee_id==LeaveRequest.employee_id).join(
                            Approver,Approver.employee_id==LeaveApproval.approver_id).join(
                            LeaveType,LeaveType.leave_type_id==LeaveRequest.leave_type_id).join(
                            Department,Employee.department_id==Department.department_id).filter(
                        LeaveRequest.employee_id==employee_id,Employee.department_id==department_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))



        
    




