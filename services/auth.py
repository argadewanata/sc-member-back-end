import os

from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt
from sqlalchemy import select
from databases import Database
from passlib.context import CryptContext
from config.database import members_table

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def authenticate_user(email: str, password: str, database: Database):
    query = select(members_table).where(members_table.c.email == email)
    user = await database.fetch_one(query)
    
    if user is None:
        return None
    
    if not pwd_context.verify(password, user["password"]):
        return None
    
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt