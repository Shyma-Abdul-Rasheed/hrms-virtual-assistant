from sqlalchemy.orm import Session
from app.models.token_revocation_model import TokenRevocation
from fastapi import HTTPException,status

def get_revoked_token(jti:str,db:Session):
    try:
        return db.query(TokenRevocation).filter(TokenRevocation.jwt_id == jti).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

def blacklist_token(revoked_token:TokenRevocation,db:Session):
    try:
        db.add(revoked_token)
        db.commit()
        db.refresh(revoked_token)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))
