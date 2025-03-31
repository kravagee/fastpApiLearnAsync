from pydantic import BaseModel


class JobCreateSchema(BaseModel):
    name: str
    description: str

class JobGetSchema(JobCreateSchema):
    id: int