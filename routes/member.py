from fastapi import APIRouter, HTTPException, Depends
from databases import Database
from sqlalchemy import select
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from models.member import Member, MemberResponse
from services.member.all import fetch_all_members
from services.member.specific import fetch_member_by_id
from config.database import get_database, members_table

member_router = APIRouter()

SECRET_KEY = "CONTOH_AJA"  # Ensure this matches your JWT secret
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

@member_router.get("/", response_model=list[MemberResponse])
async def get_all_member(database: Database = Depends(get_database)):
    try:
        return await fetch_all_members(database)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_current_user(token: str = Depends(oauth2_scheme), database: Database = Depends(get_database)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        query = select(members_table).where(members_table.c.id == user_id)
        user = await database.fetch_one(query)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@member_router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "name": current_user["nama_lengkap"],
        "email": current_user["email"]
    }

# @member_router.get("/{id}", response_model=Member)
# async def get_member_by_id(id: int, database: Database = Depends(get_database)):
#     try:
#         return await fetch_member_by_id(id, database)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))