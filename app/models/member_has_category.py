from typing import List

from pydantic import BaseModel


class MemberHasCategory(BaseModel):
    id_member: int
    id_category: List[int]


class MemberHasCategoryOut(BaseModel):
    id_member: int
    name: str
    id_category: int


class MemberHasCategoryIn(BaseModel):
    id_member: int
    name: str


class MemberWithCategory(BaseModel):
    id_member: int
    username: str
    url_portfolio: str
    category_name: str
