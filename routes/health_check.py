import logging

from typing import Union
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, HTTPException

health_check_router = APIRouter()

@health_check_router.get("/")
def read_root():
    return {"Hello": "World"}

@health_check_router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}