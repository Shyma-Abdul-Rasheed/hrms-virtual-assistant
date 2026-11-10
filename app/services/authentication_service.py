from app.core.security import hash_password,verify_password,create_jwt_token,verify_jwt_token
from fastapi import HTTPException,status
from app.schemas.employee_schema import EmployeeSignup,EmployeeLogin
from sqlalchemy.orm import Session
from app.repositories.employee_repo import existing_employee,update_employee
from app.models.token_revocation_model import TokenRevocation
from app.repositories.token_revocation_repo import blacklist_token
from app.repositories.employee_repo import get_one_employee
from datetime import datetime, timezone

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

def employee_logout(token:str, db:Session):
    try:
        payload=verify_jwt_token(token,db)
        jti=payload.get("jti")
        user_id=payload.get("user_id")
        expire=payload.get("exp")
        employee=get_one_employee(user_id,db)
        if not jti or not user_id or not expire:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid token")
        expires_at = datetime.fromtimestamp(expire,tz=timezone.utc)
        revoked_token=TokenRevocation(jwt_id=jti,employee_id=user_id,expires_at=expires_at)
        blacklist_token(revoked_token,db)
        return {"message":f"{employee.full_name} has successfully logged out"}
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))



    

    