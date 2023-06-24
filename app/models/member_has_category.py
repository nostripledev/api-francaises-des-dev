from pydantic import BaseModel


class MemberHasCategory(BaseModel):
    id_member: int
    id_category: int


class MemberWithCategory(BaseModel):
    id_member: int
    username: str
    url_portfolio: str
    category_name: str
