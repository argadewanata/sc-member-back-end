import os
import asyncio
import asyncpg

from dotenv import load_dotenv
from tqdm.asyncio import tqdm_asyncio

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

async def execute_sql(mode, sql_filepath):
    with open(sql_filepath, 'r') as f:
        sql_content = f.read()

    # Split SQL commands by semicolon
    raw_commands = sql_content.split(';')
    sql_commands = []
    
    for cmd in raw_commands:
        stripped_cmd = cmd.strip()
        if stripped_cmd:
            sql_commands.append(stripped_cmd)

    conn = await asyncpg.connect(
        host=DB_HOST, 
        port=DB_PORT,
        user=DB_USER, 
        password=DB_PASSWORD,
        database=DB_NAME, 
    )

    try:
        count = 0
        for command in tqdm_asyncio(sql_commands, desc=f"Executing {mode} operations"):
            await conn.execute(command)
            count += 1
        print(f"{count} {mode} operations executed successfully.")
    except Exception as e:
        print(f"Failed to execute {mode} operations: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Execute SQL operations on a PostgreSQL database.")
    parser.add_argument("mode", choices=["create", "insert", "alter"], help="The mode of operation.")
    parser.add_argument("sql_filepath", help="The path to the SQL file.")

    args = parser.parse_args()

    asyncio.run(execute_sql(args.mode, args.sql_filepath))