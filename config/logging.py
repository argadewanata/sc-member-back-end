import os
import logging
import httpx

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.getLogger("databases").setLevel(logging.WARNING)

if os.getenv("LOG_LEVEL") not in ["info", "trace"]:
    logging.getLogger("httpx").setLevel(logging.WARNING)