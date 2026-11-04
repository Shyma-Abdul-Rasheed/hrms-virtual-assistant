from fastapi import FastAPI, HTTPException
from app.db.connections import Base,engine
from app.routes.check_connection import router

app=FastAPI()
app.include_router(router)

