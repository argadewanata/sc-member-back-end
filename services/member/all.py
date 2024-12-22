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
            members_table.c.nomor_whatsapp
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