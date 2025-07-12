from fastapi import Depends, HTTPException, status

from app.api.models import User
from app.api.repositories import UserRepository
from app.api.schemas.authentication_schema import (
    TokenResponseSchema,
    RefreshTokenSchema,
)
from app.api.schemas.user_schema import UserBase
from app.api.utils.jwt_handler import JWTHandler


class AuthenticationController:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.__user_repo = user_repository
        self.__jwt_handler = JWTHandler()

    async def create_token(self, user: User) -> TokenResponseSchema:
        return TokenResponseSchema(
            access_token=self.__jwt_handler.create_access_token(
                user.to_dict_for_token()
            ),
            refresh_token=self.__jwt_handler.create_refresh_token(
                user.to_dict_for_token()
            ),
            token_type="bearer",
        )

    async def login(self, payload: UserBase) -> TokenResponseSchema:
        user = await self.__user_repo.get(phone_number=payload.phone_number)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        return await self.create_token(user)

    async def refresh(self, payload: RefreshTokenSchema) -> TokenResponseSchema:
        user_data = self.__jwt_handler.decode_token(payload.refresh_token)
        phone_number = user_data.get("phone_number") or None
        if not phone_number:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )
        user = await self.__user_repo.get(phone_number=phone_number)
        return await self.create_token(user)
