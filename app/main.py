from fastapi import FastAPI, HTTPException
from app.db.connections import Base,engine
from app.api.health import router
from app.api.departments import department
from app.api.employees import employee
from app.api.auth import auth
import app.models.__init__

app=FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(router)
app.include_router(auth)
app.include_router(department)
app.include_router(employee)

