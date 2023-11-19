from fastapi import APIRouter, Response, Depends

from app.auth import get_current_user, get_is_admin
from app.lib.sql import *
from typing import List

router = APIRouter(
    prefix="/network",
    tags=["network"]
)


@router.get("/", response_model=List[Network])
async def api_get_network():
    return await get_network()
