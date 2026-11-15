from app.db.connections import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends, APIRouter
from app.services.leave_balance_service import create,view_one,view_all,update,view_all_leave_balance_of_employee,view_me
from app.schemas.leave_balance_schema import LeaveBalanceCreate,LeaveBalanceUpdate,LeaveBalanceShow
from app.core.security import has_role,get_id

leave_balance=APIRouter(prefix="/api/v1/leave_balance")

@leave_balance.post("/create",response_model=LeaveBalanceShow)
def add_leave_balance(request:LeaveBalanceCreate,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return create(request,role,db)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_balance.get("/view_all_leave_balance",response_model=list[LeaveBalanceShow])
def show_all_leave_balances(db:Session = Depends(get_db),user_id:int=Depends(get_id),role:str = Depends(has_role(['admin','hr','manager']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_all(user_id,role,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_balance.get("/view_one_leave_balance/{leave_balance_id}",response_model=LeaveBalanceShow)
def show_one_leave_balances(leave_balance_id:int,user_id:int=Depends(get_id),db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr','manager']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_one(leave_balance_id,user_id,role,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_balance.get("/view_one_employee_leave_balance/{employee_id}",response_model=list[LeaveBalanceShow])
def show_employee_leave_balances(employee_id:int,db:Session = Depends(get_db),user_id:int=Depends(get_id),role:str = Depends(has_role(['admin','hr','manager']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return view_all_leave_balance_of_employee(employee_id,user_id,role,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_balance.get("/view_my_leave_balance",response_model=list[LeaveBalanceShow])
def show_one_leave_balances(employee_id:int = Depends(get_id),db:Session = Depends(get_db)):
    try:
        if employee_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="No such employee")
        return view_me(employee_id,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@leave_balance.put("/update_leave_balance/{leave_balance_id}",response_model=LeaveBalanceShow)
def change_leave_balance(leave_balance_id:int,request:LeaveBalanceUpdate,db:Session = Depends(get_db),role:str = Depends(has_role(['admin','hr']))):
    try:
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        return update(leave_balance_id,request,role,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


