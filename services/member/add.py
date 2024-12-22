from passlib.context import CryptContext
from sqlalchemy import insert, select
from databases import Database
from fastapi import HTTPException
from models.member import MemberCreate
from config.database import members_table

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def add_new_member(member_data: MemberCreate, database: Database):
    # Check if email already exists
    existing_member_query = select(members_table).where(members_table.c.email == member_data.email)
    existing_member = await database.fetch_one(existing_member_query)

    if existing_member:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = pwd_context.hash(member_data.nomor_whatsapp)
    query = insert(members_table).values(
        nama_lengkap=member_data.nama_lengkap,
        email=member_data.email,
        nomor_whatsapp=member_data.nomor_whatsapp,
        password=hashed_password
    )
    try:
        await database.execute(query)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error adding new member: {e}")
