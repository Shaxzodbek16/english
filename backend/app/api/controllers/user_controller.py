from fastapi import Depends, status, HTTPException

from app.api.models import User
from app.api.repositories import UserRepository
from app.api.schemas import QueryParamsSchema, UserListResponseSchema, UserUpdateSchema
from app.api.schemas.user_schema import UserResponseSchema


class UserController:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.__user_repo: UserRepository = user_repo

    @staticmethod
    async def check_admin(user: User):
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

    async def get(self, phone_number: int) -> UserResponseSchema:
        user = await self.__user_repo.get(phone_number=phone_number)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return UserResponseSchema.model_validate(user)

    async def get_by_telegram_id(self, telegram_id: int) -> UserResponseSchema:
        user = await self.__user_repo.get_by_telegram_id(telegram_id=telegram_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return UserResponseSchema.model_validate(user)

    async def list(self, params: QueryParamsSchema) -> UserListResponseSchema:
        users = await self.__user_repo.list(params=params)
        return UserListResponseSchema(
            page=params.page,
            size=params.size,
            search=params.search,
            filter=params.filter,
            sort=params.sort,
            total=len(users),
            items=[UserResponseSchema.model_validate(user) for user in users],
        )

    async def update(
        self, phone_number: int, payload: UserUpdateSchema
    ) -> UserResponseSchema:
        return UserResponseSchema.model_validate(
            await self.__user_repo.update(phone_number=phone_number, payload=payload)
        )
