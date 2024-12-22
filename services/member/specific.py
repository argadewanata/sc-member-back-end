from sqlalchemy import select
from databases import Database
from models.member import Member
from config.database import members_table

async def fetch_member_by_id(id: int, database: Database):
    query = select(members_table).where(members_table.c.id == id)
    member = await database.fetch_one(query)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return Member(**member)