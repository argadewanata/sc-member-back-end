import os
import sys
import uvicorn
import logging
import asyncio

from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()

async def start_server():
    load_dotenv()
    # Set default values and override with .env values if exist
    host = os.getenv("BE_HOST", "0.0.0.0")
    port = int(os.getenv("BE_PORT", 8000))
    log_level = os.getenv("LOG_LEVEL", "warning")

    logging.info(f"Starting BE Server on {host}:{port}...")

    config = uvicorn.Config(
        "main:app",
        host=host,
        port=port,
        reload=False,
        log_level=log_level,
        workers=4,
    )

    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    # Check the operating system and select an appropriate event loop
    CURRENT_PLATFORM = sys.platform
    if CURRENT_PLATFORM.startswith('linux'):
        import uvloop
        logging.info(f"=== [Running on {CURRENT_PLATFORM} with uvloop as event loop] ===")
        uvloop.run(start_server())
    else:
        logging.info(f"=== [Running on {CURRENT_PLATFORM} with asyncio as event loop] ===")
        asyncio.run(start_server())