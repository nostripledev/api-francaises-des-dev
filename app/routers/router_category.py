from typing import List

from fastapi import APIRouter

from app.lib.sql import *
from app.models import *

router = APIRouter(
    prefix="/category",
    tags=["category"]
)


@router.get("/", response_model=List[Category])
async def api_get_categories():
    return await get_categories()
