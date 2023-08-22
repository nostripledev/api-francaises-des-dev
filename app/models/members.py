from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class MemberById(BaseModel):
    id: int


class MemberIn(MemberById):
    username: str
    firstname: Optional[str]
    lastname: Optional[str]
    description: Optional[str]
    mail: Optional[str]
    url_portfolio: Optional[str]


class MemberOut(MemberIn):
    id: str
    date_activated: Optional[datetime] = None


class Member(MemberOut):
    date_deleted: Optional[datetime] = None


class GetMembers(BaseModel):
    id: int
    username: str
    url_portfolio: str
