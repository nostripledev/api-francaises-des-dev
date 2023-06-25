from pydantic import BaseModel


class MemberHasNetwork(BaseModel):
    id_member: int
    id_network: int
    url: str


class GetMemberHasNetwork(BaseModel):
    name: str
    url: str
