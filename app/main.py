from typing import List

from app.lib.sql import get_members, get_member_by_id, post_member, patch_member_update
from app.lib.sql import  get_categories, post_category, get_members_category, post_add_category_on_member, get_category_of_member_by_id, delete_category_delete_by_member
from app.lib.sql import get_network_of_member_by_id , get_network, post_network_on_member, delete_network_delete_by_member

from fastapi import FastAPI, Response
from app.models import MemberIn, MemberOut, Category, CategoryOut, MemberWithCategory, MemberHasCategoryIn, GetMemberHasNetwork, MemberById, Network, MemberHasNetwork, MemberHasCategory, MemberHasNetworkIn

app = FastAPI()


@app.get("/members", response_model=List[MemberWithCategory])
def api_get_members():
    return get_members()


@app.get("/members/{id:int}", response_model=MemberIn)
def api_get_member_by_id(id: int):
    member = get_member_by_id(id)
    if member is None:
        return Response(status_code=404)
    return member


@app.post("/members", response_model=MemberOut)
def api_post_member(member: MemberIn):
    result = post_member(member)
    if result is not None:
        return Response(status_code=400)
    return Response(status_code=200)


@app.patch("/members/update")
def api_patch_member_update(member: MemberOut):
    result = patch_member_update(member)
    if result is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@app.get("/categories", response_model=List[Category])
def api_get_categories():
    return get_categories()


@app.post("/categories")
def api_post_category(category: CategoryOut):
    result = post_category(category)
    if result is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@app.get("/members/category={name:str}")
def api_get_members_category(name: str):
    member = get_members_category(name)
    if member is None:
        return Response(status_code=404)
    return member


@app.post("/members/category")
def api_post_add_category_on_member(member: MemberHasCategoryIn):
    category = post_add_category_on_member(member)
    if category is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@app.get("/network", response_model=List[Network])
def api_get_network():
    return get_network()


@app.get("/members/network", response_model=List[GetMemberHasNetwork])
def api_get_network_of_member(id_member: int):
    return get_network_of_member_by_id(id_member)


@app.get("/members/list_category", response_model=List[CategoryOut])
def api_get_category_of_member_by_id(member: MemberById):
    return get_category_of_member_by_id(member)


@app.post("/members/network")
def api_post_network_on_member(member: MemberHasNetwork):
    network = post_network_on_member(member)
    if network is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@app.delete("/members/category_delete")
def api_delete_category_delete_by_member(member: MemberHasCategory):
    verif = delete_category_delete_by_member(member)
    if verif is not None:
        return Response(status_code=400)
    return Response(status_code=200)


@app.delete("/members/network_delete")
def api_delete_network_delete_by_member(member: MemberHasNetworkIn):
    verif = delete_network_delete_by_member(member)
    if verif is not None:
        return Response(status_code=400)
    return Response(status_code=200)
