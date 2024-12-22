from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, insert, update
from databases import Database
from pydantic import BaseModel, EmailStr
from config.database import get_database, members_table
from services.auth import authenticate_user, create_access_token
from passlib.context import CryptContext
from services.member.card import get_current_user
from models.auth import PasswordChangeRequest

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    needs_password_change: bool

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    whatsapp: str
    password: str

@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, database: Database = Depends(get_database)):
    user = await authenticate_user(request.email, request.password, database)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token(
        data={"sub": user["email"], "id": user["id"]}
    )
    
    # Check if the password is the default hashed phone number
    needs_password_change = pwd_context.verify(user["nomor_whatsapp"], user["password"])
    
    return {"access_token": access_token, "token_type": "bearer", "needs_password_change": needs_password_change}

@auth_router.post("/register")
async def register(request: RegisterRequest, database: Database = Depends(get_database)):
    hashed_password = pwd_context.hash(request.password)
    current_time = datetime.now()  
    query = insert(members_table).values(
        nama_lengkap=request.name,
        email=request.email,
        nomor_whatsapp=request.whatsapp,
        password=hashed_password,
        timestamp_daftar=current_time  
    )
    try:
        await database.execute(query)
        return {"message": "Registration successful!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to register user")

@auth_router.put("/change-password")
async def change_password(request: PasswordChangeRequest, current_user: dict = Depends(get_current_user), database: Database = Depends(get_database)):
    hashed_password = pwd_context.hash(request.newPassword)
    query = (
        update(members_table)
        .where(members_table.c.id == current_user["id"])
        .values(password=hashed_password)
    )
    try:
        await database.execute(query)
        return {"message": "Password changed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to change password")