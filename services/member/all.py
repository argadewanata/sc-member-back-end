import logging
from sqlalchemy import select
from databases import Database
from models.member import MemberResponse
from config.database import members_table, database

async def fetch_all_members(database: Database):
    logging.info("Fetching all members...")
    query = select(members_table.c.id, members_table.c.nama_lengkap, members_table.c.email, members_table.c.nomor_whatsapp)
    rows = await database.fetch_all(query)
    members = [MemberResponse(**row) for row in rows]
    logging.info("Members fetched successfully")
    return members