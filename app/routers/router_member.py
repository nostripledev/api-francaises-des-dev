from typing import List

from fastapi import APIRouter
from starlette.responses import Response

from app.lib.function import verifIsPngAndJpeg
from app.lib.sql import *
from app.models import *
from app.models.member_has_category import MemberHasCategoryOut

router = APIRouter(
    prefix="/member",
    tags=["member"]
)


@router.get("/", response_model=List[MemberWithCategory])
async def api_get_members():
    return await get_members()


@router.get("/{id:int}", response_model=MemberIn)
async def api_get_member_by_id(id: int):
    member = await get_member_by_id(id)
    if member is None:
        return Response(status_code=404)
    return member


@router.patch("/")
async def api_patch_member_update(member: MemberOut):
    result = await patch_member_update(member)
    if result is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@router.patch("/image_portfolio")
async def api_add_image_portfolio(file: UploadFile, id_member: int):
    if file.size > 200 * 10000:
        return Response(status_code=413)
    if file.content_type not in ['image/jpeg', 'image/png']:
        return Response(status_code=415)
    if verifIsPngAndJpeg(file) is None:
        return Response(status_code=415)
    verif = await add_image_portfolio(file, id_member)
    if verif is not None:
        return Response(status_code=500)
    return Response(status_code=200)


@router.get("/image_portfolio_by_id")
async def api_get_image_portfolio_by_id_member(id_member: int):
    return Response(content=await get_image_by_id_member(id_member), media_type="image/jpg")


@router.post("/category")
async def api_post_add_category_on_member(member: MemberHasCategory):
    category = await post_add_category_on_member(member)
    if category is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@router.get("/list_category/{id:int}", response_model=List[CategoryOut])
async def api_get_category_of_member_by_id(id: int):
    return await get_category_of_member_by_id(id)


@router.get("/category/{id:int}", response_model=List[MemberHasCategoryOut])
async def api_get_member_has_category_by_id_member(id: int):
    return await get_member_has_category_by_id_member(id)


@router.delete("/category")
async def api_delete_category_delete_by_member(member: MemberHasCategory):
    verif = await delete_category_delete_by_member(member)
    if verif is not None:
        return Response(status_code=400)
    return Response(status_code=200)


@router.get("/category={name:str}")
async def api_get_members_category(name: str):
    member = await get_members_category(name)
    if member is None:
        return Response(status_code=404)
    return member


@router.get("/network/{id:int}", response_model=List[GetMemberHasNetwork])
async def api_get_network_of_member(id: int):
    return await get_network_of_member_by_id(id)


@router.post("/network")
async def api_post_network_on_member(member: MemberHasNetwork):
    network = await post_network_on_member(member)
    if network is not None:
        return Response(status_code=400)
    return Response(status_code=201)
