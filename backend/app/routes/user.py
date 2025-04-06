from fastapi import APIRouter 
from app.config.database import connection 
from models.index import user


user = APIRouter()

@user.get("/")
async def read_data():
    return connection.execute(user.select()).fetchall()   