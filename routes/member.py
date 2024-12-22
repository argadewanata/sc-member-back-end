from fastapi import APIRouter, HTTPException, Depends, Query
from databases import Database
from services.member.all import fetch_all_members_paginated, search_members
from models.member import Member, MemberResponse, PaginatedMembersResponse, MemberCreate
from services.member.specific import fetch_member_by_id
from services.member.card import get_current_user
from services.member.add import add_new_member
from config.database import get_database,members_table

member_router = APIRouter()

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