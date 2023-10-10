from typing import List

from pydantic import BaseModel


class MemberHasNetworkIn(BaseModel):
    id_member: int
    id_network: List[int]


class MemberHasNetwork(BaseModel):
    id_member: int
    id_network: List[int]
    url: List[str]


class GetMemberHasNetwork(BaseModel):
    name: str
    url: str
    id_network: int
