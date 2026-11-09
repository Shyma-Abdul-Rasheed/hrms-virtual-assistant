from app.core.security import hash_password,verify_password,create_jwt_token
from fastapi import HTTPException,status
from app.schemas.employee_schema import EmployeeSignup,EmployeeLogin
from sqlalchemy.orm import Session
from app.repositories.employee_repo import existing_employee,update_employee

async def employee_signup(request:EmployeeSignup,db:Session):
    try:
        user=existing_employee(request.email,db)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Error in provided information")
        if request.full_name==user.full_name and request.email==user.email:
            hash=hash_password(request.password)
            user.hashed_password=hash
            return update_employee(user,db)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Error in provided information")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    
async def employee_login(request:EmployeeLogin,db:Session):
    try:
        user=existing_employee(request.email,db)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid credentials")
        
        match=verify_password(user.hashed_password,request.password)
        if match is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid credentials")
        token=create_jwt_token(user.employee_id,user.role)
        return {"message":f"{user.full_name} has successfully logged in","token":token}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    

    