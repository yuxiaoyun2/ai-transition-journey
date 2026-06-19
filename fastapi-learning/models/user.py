from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str


class UserUpdate(BaseModel):
    name: str
