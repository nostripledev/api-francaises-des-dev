from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class MemberById(BaseModel):
    id: int


class MemberIn(BaseModel):
    username: str
    firstname: str
    lastname: str
    description: str
    mail: str
    url_portfolio: str


class MemberOut(MemberIn):
    id: str
    date_activated: Optional[datetime] = None


class Member(MemberOut):
    date_deleted: Optional[datetime] = None


class GetMembers(BaseModel):
    id: int
    username: str
    url_portfolio: str
