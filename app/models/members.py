from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class MemberIn(BaseModel):
    username: str
    firstname: str
    lastname: str
    mail: str
    url_portfolio: str


class MemberOut(MemberIn):
    date_activated: Optional[datetime] = None


class Member(MemberOut):
    date_deleted: Optional[datetime] = None
