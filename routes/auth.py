from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from databases import Database
from pydantic import BaseModel
from config.database import get_database
from services.auth import authenticate_user, create_access_token

auth_router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, database: Database = Depends(get_database)):
    user = await authenticate_user(request.email, request.password, database)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token(
        data={"sub": user["email"], "id": user["id"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}