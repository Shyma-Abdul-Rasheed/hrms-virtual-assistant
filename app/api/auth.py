from app.db.connections import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends, APIRouter
from app.services.authentication_service import employee_login,employee_signup
from app.schemas.employee_schema import EmployeeLogin,EmployeeSignup,EmployeeShow


auth=APIRouter(prefix="/api/v1/auth")

@auth.post("/signup",response_model=EmployeeShow)
async def signup(request:EmployeeSignup,db:Session=Depends(get_db)):
    try:
        return await employee_signup(request,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    finally:
        db.close()
    
@auth.post("/login",response_model=dict)
async def login(request:EmployeeLogin,db:Session=Depends(get_db)):
    try:
        return await employee_login(request,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    finally:
        db.close()


    