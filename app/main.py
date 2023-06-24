from typing import List

from app.lib.sql import get_members, get_member_by_id, post_member

from fastapi import FastAPI, Response
from app.models import Member, MemberIn, MemberOut, GetMembers

app = FastAPI()


@app.get("/members", response_model=List[GetMembers])
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
