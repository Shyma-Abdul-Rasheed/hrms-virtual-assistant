from dotenv import load_dotenv
from argon2 import PasswordHasher
from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
import os
import jwt

load_dotenv()
ph=PasswordHasher()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

def hash_password(text:str)->str:
    return ph.hash(text)

def verify_password(hash:str,plain:str)->bool:
    try:
        return ph.verify(hash,plain)
    except:
        return False
    
def create_jwt_token(user_id:int,user_role:str)->str:
    try:
        payload={"user_id":user_id,"user_role":user_role}
        token=jwt.encode(payload,os.getenv("SECRET_KEY"),algorithm="HS256")
        return token
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    
def verify_jwt_token(token:str)->dict:
    try:
        payload=jwt.decode(token,os.getenv("SECRET_KEY"),algorithms=["HS256"])
        return payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    
def get_id(token:str=Depends(oauth2_scheme))->int:
    payload=verify_jwt_token(token)
    if payload is None:
        return None
    else:
        return payload.get("user_id")
    
def has_role(allowed_roles:list[str]):
    def get_role(token:str=Depends(oauth2_scheme))->str:
        payload=verify_jwt_token(token)
        if payload is None:
            return None
        else:
            role= payload.get("user_role")
            if role not in allowed_roles:
                return None
        return role
    return get_role