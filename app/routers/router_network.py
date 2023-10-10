from fastapi import APIRouter, Response

from app.lib.sql import *
from typing import List

router = APIRouter(
    prefix="/network",
    tags=["network"]
)


@router.get("/", response_model=List[Network])
async def api_get_network():
    return await get_network()
