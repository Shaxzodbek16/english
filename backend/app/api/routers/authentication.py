from fastapi import APIRouter, Depends, status

from app.api.controllers.authentication_controller import AuthenticationController
from app.api.models import User
from app.api.repositories.user_repository import UserRepository
from app.api.utils.jwt_handler import get_current_user, JWTHandler

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
)
async def register(auth_controller: AuthenticationController = Depends()):
    pass


@router.post("/login/")
async def login(
    current_user: User = Depends(get_current_user),
):
    return current_user.first_name


@router.post("/me/")
async def get_token(
    number: int,
    repo: UserRepository = Depends(),
):
    user = await repo.get(number)
    return JWTHandler().create_access_token(user.to_dict_for_token())
