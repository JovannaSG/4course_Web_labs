from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str
    task: str


class KeycloakToken(BaseModel):
    access_token: str
    expires_in: int
    refresh_expires_in: int
    refresh_token: str
    token_type: str
    not_before_policy: int = Field(alias="not-before-policy")
    session_state: str
    scope: str
