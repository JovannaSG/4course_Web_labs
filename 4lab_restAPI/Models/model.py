from pydantic import BaseModel


class UserCreate(BaseModel):
    #id: int
    name: str
    task: str

class AuthKeycloak(BaseModel):
    pass
