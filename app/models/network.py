from pydantic import BaseModel


class NetworkOut(BaseModel):
    name: str


class Network(NetworkOut):
    id: int
