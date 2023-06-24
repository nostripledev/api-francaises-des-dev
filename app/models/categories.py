from pydantic import BaseModel


class CategoryOut(BaseModel):
    name: str


class Category(CategoryOut):
    id: int
