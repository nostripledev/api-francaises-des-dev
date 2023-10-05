from fastapi import APIRouter, Response

from app.lib.sql import *
from typing import List

router = APIRouter(
    prefix="/network",
    tags=["network"]
)


@router.get("/", response_model=List[Network])
async def api_get_network():
    print("c'est moi")
    return await get_network()


@router.delete("/")
async def api_delete_network_delete_by_member(member: MemberHasNetworkIn):
    verif = await delete_network_delete_by_member(member)
    if verif is not None:
        return Response(status_code=400)
    return Response(status_code=200)
