from typing import List

from fastapi import FastAPI
from app.models import Member, MemberIn, MemberOut

app = FastAPI()


@app.get("/", response_model=List[MemberOut])
def read_root():
    return [MemberOut(username="koko",firstname="raphaelle",lastname="huynh",mail="koko@gmail.com",url_portfolio="http://wesh.com"),MemberOut(username="koko",firstname="raphaelle",lastname="huynh",mail="koko@gmail.com",url_portfolio="http://wesh.com")]


@app.post("/members", response_model=MemberOut)
def post_member(member: MemberIn):
    return MemberOut(**member.dict())