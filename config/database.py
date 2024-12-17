import os
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Date, Boolean, CheckConstraint, CHAR, TIMESTAMP
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

database = Database(DATABASE_URL)

metadata = MetaData()

members_table = Table(
    "members",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("timestamp_daftar", TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP"),
    Column("email", Text, nullable=False),
    Column("nama_lengkap", String(255), nullable=False),
    Column("password", Text, nullable=False),
    Column("provinsi", String(255), nullable=False),
    Column("kota", String(255), nullable=False),
    Column("kecamatan", String(255)),
    Column("kelurahan", String(255)),
    Column("alamat_lengkap", Text, nullable=False),
    Column("nomor_whatsapp", String(20), nullable=False),
    Column("jenis_kelamin", CHAR(1), nullable=False),
    Column("tanggal_lahir", Date, nullable=False),
    Column("pendidikan_terakhir", Integer, nullable=False),
    Column("profesi", String(255)),
    Column("referensi", Text),
    Column("harapan", Text),
    Column("is_verified", Boolean, server_default="false"),
    Column("is_active", Boolean, server_default="false"),
    Column("is_admin", Boolean, server_default="false"),
    CheckConstraint("jenis_kelamin IN ('L', 'P')", name='check_jenis_kelamin'),
    CheckConstraint("pendidikan_terakhir BETWEEN 0 AND 9", name='check_pendidikan_terakhir')
)

async def get_database() -> Database:
    try:
        await database.connect()
        yield database
    finally:
        await database.disconnect()