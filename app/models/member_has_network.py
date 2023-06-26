from pydantic import BaseModel


class MemberHasNetworkIn(BaseModel):
    id_member: int
    id_network: int


class MemberHasNetwork(MemberHasNetworkIn):
    url: str


class GetMemberHasNetwork(BaseModel):
    name: str
    url: str
