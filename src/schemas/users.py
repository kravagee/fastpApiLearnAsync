from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    name: str
    password: str

class UserGetSchema(UserCreateSchema):
    id: int