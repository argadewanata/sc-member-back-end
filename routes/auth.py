from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from databases import Database
from passlib.context import CryptContext
from pydantic import BaseModel
from config.database import members_table, get_database

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str
    name: str
    email: str
    id: int

@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, database: Database = Depends(get_database)):
    query = select(members_table).where(members_table.c.email == request.email)
    user = await database.fetch_one(query)
    
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    hashed_password = user["password"]
    
    if not pwd_context.verify(request.password, hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    return {
        "message": "Login successful",
        "name": user["nama_lengkap"],
        "email": user["email"],
        "id": user["id"]
    }