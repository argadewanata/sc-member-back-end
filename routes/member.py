from fastapi import APIRouter, HTTPException, Depends
from databases import Database
from fastapi.security import OAuth2PasswordBearer
from models.member import Member, MemberResponse
from services.member.all import fetch_all_members
from services.member.specific import fetch_member_by_id
from services.member.card import get_current_user
from config.database import get_database

member_router = APIRouter()

@member_router.get("/card")
async def read_users_card(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "name": current_user["nama_lengkap"],
        "email": current_user["email"]
    }

@member_router.get("/", response_model=list[MemberResponse])
async def get_all_member(database: Database = Depends(get_database)):
    try:
        return await fetch_all_members(database)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@member_router.get("/detail/{id}", response_model=Member)
async def get_member_by_id(id: int, database: Database = Depends(get_database)):
    try:
        return await fetch_member_by_id(id, database)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))