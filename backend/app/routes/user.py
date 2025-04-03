from fastapi import APIRouter 
from config.db import connection 
from models.index import user


user = APIRouter()

@user.get("/")
async def read_data():
    return connection.execute(user.select()).fetchall()   