from pydantic import BaseModel


class MemberHasCategory(BaseModel):
    id_member: int
    id_category: int
