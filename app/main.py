from fastapi import FastAPI, HTTPException
from app.db.connections import Base,engine
from app.routes.check_connection import router
import app.models.__init__

app=FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(router)

