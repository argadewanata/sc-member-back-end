from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select, update
from databases import Database
from services.member.all import fetch_all_members_paginated, search_members
from models.member import Member, MemberResponse, PaginatedMembersResponse, MemberCreate
from services.member.specific import fetch_member_by_id
from services.member.card import get_current_user
from services.member.add import add_new_member
from config.database import get_database,members_table
from passlib.context import CryptContext

member_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@member_router.get("/card")
async def read_users_card(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "name": current_user["nama_lengkap"],
        "email": current_user["email"],
        "is_admin": current_user["is_admin"],
        "nomor_whatsapp": current_user["nomor_whatsapp"],
    }

@member_router.get("/", response_model=PaginatedMembersResponse)
async def get_all_member(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    database: Database = Depends(get_database)
):
    try:
        return await fetch_all_members_paginated(database, page, size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@member_router.get("/search", response_model=PaginatedMembersResponse)
async def search_member(
    search: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    database: Database = Depends(get_database)
):
    try:
        return await search_members(database, search, page, size)
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

@member_router.put("/update/{id}")
async def update_member(id: int, member_data: dict, database: Database = Depends(get_database)):
    try:
        query = (
            members_table.update()
            .where(members_table.c.id == id)
            .values(is_verified=member_data['is_verified'], is_active=member_data['is_active'])
        )
        await database.execute(query)
        return {"message": "Member updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@member_router.post("/add")
async def add_member(member_data: MemberCreate, database: Database = Depends(get_database)):
    try:
        await add_new_member(member_data, database)
        return {"message": "Member added successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@member_router.put("/reset-password/{id}")
async def reset_password(id: int, current_user: dict = Depends(get_current_user), database: Database = Depends(get_database)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to reset password")
    try:
        query = select(members_table.c.nomor_whatsapp).where(members_table.c.id == id)

        member = await database.fetch_one(query)

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        hashed_password = pwd_context.hash(member["nomor_whatsapp"])

        update_query = (
            update(members_table)
            .where(members_table.c.id == id)
            .values(password=hashed_password)
        )
        await database.execute(update_query)
        return {"message": "Password reset to default successfully"}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to reset password: {str(e)}")