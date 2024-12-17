import asyncio
import asyncpg
import bcrypt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

async def add_password_column():
    conn = await asyncpg.connect(
        user=DB_USER, password=DB_PASSWORD,
        database=DB_NAME, host=DB_HOST, port=DB_PORT
    )

    try:
        await conn.execute("""
            ALTER TABLE members
            ADD COLUMN IF NOT EXISTS password VARCHAR(150) NOT NULL DEFAULT '';
        """)
        print("Password column added successfully.")
    except Exception as e:
        print(f"Failed to add password column: {e}")
    finally:
        await conn.close()

async def update_passwords():
    conn = await asyncpg.connect(
        host=DB_HOST, 
        port=DB_PORT,
        database=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD,
    )

    try:
        # Fetch all members
        members = await conn.fetch("SELECT id, nomor_whatsapp FROM members")
        
        for member in members:
            hashed_password = bcrypt.hashpw(member['nomor_whatsapp'].encode('utf-8'), bcrypt.gensalt())
            await conn.execute("""
                UPDATE members
                SET password = $1
                WHERE id = $2
            """, hashed_password.decode('utf-8'), member['id'])
        
        print(f"Updated passwords for {len(members)} members.")
    except Exception as e:
        print(f"Failed to update passwords: {e}")
    finally:
        await conn.close()

async def main():
    await add_password_column()
    await update_passwords()

asyncio.run(main())