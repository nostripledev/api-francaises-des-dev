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


@router.get("/{id:int}", response_model=List[GetMemberHasNetwork])
async def api_get_network_of_member(id: int):
    return await get_network_of_member_by_id(id)


@router.post("/{id:int}")
async def api_post_network_on_member(member: MemberHasNetwork):
    network = await post_network_on_member(member)
    if network is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@router.delete("/")
async def api_delete_network_delete_by_member(member: MemberHasNetworkIn):
    verif = await delete_network_delete_by_member(member)
    if verif is not None:
        return Response(status_code=400)
    return Response(status_code=200)
