from typing import List

from fastapi import APIRouter
from starlette.responses import Response

from app.lib.sql import *
from app.models import *
from app.auth.auth import *

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.post("/category")
async def api_post_category(category: CategoryOut, is_admin_user: bool = Depends(get_is_admin)):
    result = await post_category(category)
    if result is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@router.post("/network")
async def api_post_network(name_network: NetworkOut, is_admin_user: bool = Depends(get_is_admin)):
    if await add_new_network(name_network):
        return Response(status_code=201)
    return Response(status_code=400)


@router.delete("/category")
async def api_delete_category(name: str, current_user: dict = Depends(get_current_user), is_admin_user: bool = Depends(get_is_admin)):
    if await delete_category(name) is not None:
        return Response(status_code=400)
    return Response(status_code=200)


@router.delete("/network")
async def api_delete_network(name: str, is_admin_user: bool = Depends(get_is_admin)):
    if await delete_network(name) is not None:
        return Response(status_code=400)
    return Response(status_code=200)


@router.patch("/member/validate")
async def api_validate_member(id_member: int, current_user: dict = Depends(get_current_user), is_admin_user: bool = Depends(get_is_admin)):
    if await validate_member(id_member) is not None:
        return Response(status_code=400)
    return Response(status_code=200)


@router.patch("/member/ban")
async def api_ban_member(id_member: int, current_user: dict = Depends(get_current_user), is_admin_user: bool = Depends(get_is_admin)):
    if await ban_member(id_member) is not None:
        return Response(status_code=400)
    return Response(status_code=200)
