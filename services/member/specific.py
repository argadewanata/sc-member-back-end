import logging
from sqlalchemy import select
from databases import Database
from fastapi import HTTPException
from models.member import Member
from config.database import members_table, database

async def fetch_member_by_id(id: int, database: Database):
    logging.info(f"Fetching member with ID: {id}")
    query = select(members_table).where(members_table.c.id == id)
    row = await database.fetch_one(query)
    if row is None:
        logging.warning(f"Member with ID {id} not found")
        raise HTTPException(status_code=404, detail="Member not found")
    logging.info(f"Member with ID {id} fetched successfully")
    return Member(**row)