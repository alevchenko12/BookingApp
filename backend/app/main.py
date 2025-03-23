#FastAPI: A lightweight web framework to create APIs in Python.
#SQLAlchemy: Used for interacting with the MySQL database.
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection
#REMOVE TO SECRETS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
DATABASE_URL = "mysql+pymysql://root:coursE2025!@localhost/test_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# API to fetch all users
@app.get("/users")
def get_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return users

# Run the server: `uvicorn app.main:app --reload`

