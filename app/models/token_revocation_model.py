from sqlalchemy import Column, Integer, String, DateTime
from app.db.connections import Base


class TokenRevocation(Base):
    __tablename__ = "token_revocations"
    jwt_id= Column(String, primary_key=True, nullable=False)
    employee_id = Column(Integer, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)