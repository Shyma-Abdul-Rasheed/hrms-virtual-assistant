from pydantic import BaseModel,Field

class LeaveBalanceCreate(BaseModel):
    employee_code: str
    leave_type_name: str
    year: int
    entitlement_days: int = Field(ge=0)
    used_days: int = Field(default=0, ge=0)
    class Config:
        from_attributes=True

class LeaveBalanceUpdate(BaseModel):
    entitlement_days: int | None = Field(default=None, ge=0)
    used_days: int | None = Field(default=None, ge=0)
    class Config:
        from_attributes=True

class LeaveBalanceShow(BaseModel):
    leave_balance_id:int
    employee_code: str
    full_name:str
    department_name:str
    leave_type_name: str
    year: int
    entitlement_days: int
    used_days: int
    balance_days: int
    class Config:
        from_attributes=True

