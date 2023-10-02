from typing import List

from fastapi import APIRouter
from starlette.responses import Response

from app.lib.sql import *
from app.models import *

router = APIRouter(
    prefix="/category",
    tags=["category"]
)


@router.get("/", response_model=List[Category])
async def api_get_categories():
    return await get_categories()


@router.post("/")
async def api_post_category(category: CategoryOut):
    result = await post_category(category)
    if result is not None:
        return Response(status_code=400)
    return Response(status_code=201)
