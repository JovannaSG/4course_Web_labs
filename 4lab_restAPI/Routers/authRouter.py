from fastapi import APIRouter
from Models.model import AuthKeycloak


auth_router = APIRouter(
    prefix="/auth"
)


@auth_router.get("/")
def root():
    return {"Message": "OK"}
