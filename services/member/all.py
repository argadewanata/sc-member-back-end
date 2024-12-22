import logging
from sqlalchemy import select, func
from databases import Database
from models.member import MemberResponse
from config.database import members_table

async def fetch_all_members_paginated(database: Database, page: int, size: int):
    offset = (page - 1) * size
    query = (
        select(
            members_table.c.id,
            members_table.c.nama_lengkap,
            members_table.c.email,
            members_table.c.nomor_whatsapp,
            members_table.c.is_verified,
            members_table.c.is_active,
            members_table.c.is_admin
        )
        .offset(offset)
        .limit(size)
    )
    rows = await database.fetch_all(query)

    try:
        total_query = select(func.count()).select_from(members_table)
        total_result = await database.fetch_one(total_query)
        total = total_result[0] if total_result else 0
    except Exception as e:
        logging.error(f"Error fetching total count: {e}")
        total = 0

    members = [MemberResponse(**row) for row in rows]
    logging.info("Members fetched successfully")
    return {"members": members, "total": total}

async def search_members(database: Database, search: str, page: int, size: int):
    logging.info(f"Searching members with query '{search}' for page {page} with size {size}...")
    offset = (page - 1) * size

    # Construct the query with search filtering
    query = (
        select(
            members_table.c.id,
            members_table.c.nama_lengkap,
            members_table.c.email,
            members_table.c.nomor_whatsapp,
            members_table.c.is_verified,
            members_table.c.is_active,
            members_table.c.is_admin
        )
        .where(
            (members_table.c.nama_lengkap.ilike(f"%{search}%")) |
            (members_table.c.email.ilike(f"%{search}%")) |
            (members_table.c.nomor_whatsapp.ilike(f"%{search}%"))
        )
        .offset(offset)
        .limit(size)
    )
    rows = await database.fetch_all(query)

    try:
        # Total count query with search filtering
        total_query = select(func.count()).select_from(members_table).where(
            (members_table.c.nama_lengkap.ilike(f"%{search}%")) |
            (members_table.c.email.ilike(f"%{search}%")) |
            (members_table.c.nomor_whatsapp.ilike(f"%{search}%"))
        )
        total_result = await database.fetch_one(total_query)
        total = total_result[0] if total_result else 0
    except Exception as e:
        logging.error(f"Error fetching total count: {e}")
        total = 0

    members = [MemberResponse(**row) for row in rows]
    logging.info("Search completed successfully")
    return {"members": members, "total": total}