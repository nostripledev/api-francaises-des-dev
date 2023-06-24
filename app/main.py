from typing import List

from app.lib.sql import get_members, get_member_by_id, post_member
from app.lib.sql import  get_categories, post_category, get_members_category

from fastapi import FastAPI, Response
from app.models import MemberIn, MemberOut, Category, CategoryOut, MemberWithCategory

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

