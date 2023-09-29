from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class MemberById(BaseModel):
    id: int


class Member(MemberById):
    firstname: Optional[str]
    lastname: Optional[str]
    description: Optional[str]
    mail: Optional[str]
    url_portfolio: Optional[str]


class MemberIn(Member):
    username: Optional[str]


class MemberOut(MemberIn):
    date_activated: Optional[datetime] = None
    date_deleted: Optional[datetime] = None


class GetMembers(BaseModel):
    id: int
    username: str
    url_portfolio: str
