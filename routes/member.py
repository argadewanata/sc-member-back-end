import logging
import os
import config.logging

from fastapi import APIRouter, HTTPException, Depends
from databases import Database
from sqlalchemy import select, Table, MetaData, Column, Integer, String
from models.member import MemberResponse
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
database = Database(DATABASE_URL)

metadata = MetaData()

members_table = Table(
    "members",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nama_lengkap", String(255)),
    Column("email", String),
    Column("nomor_whatsapp", String(20)),
)

member_router = APIRouter()

async def get_database() -> Database:
    database = Database(DATABASE_URL)
    try:
        await database.connect()
        yield database
    finally:
        await database.disconnect()

@member_router.get("/get_all_member", response_model=list[MemberResponse])
async def get_all_member(database: Database = Depends(get_database)):
    logging.info("Fetching all members...")
    query = select(members_table.c.id, members_table.c.nama_lengkap, members_table.c.email, members_table.c.nomor_whatsapp)
    try:
        rows = await database.fetch_all(query)
        members = []
        for row in rows:
            members.append(MemberResponse(**row))
        logging.info("Members fetched successfully")
        return members
    except Exception as e:
        logging.error(f"Error fetching members: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")