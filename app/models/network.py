from pydantic import BaseModel


class Network(BaseModel):
    id: int
    name: str
