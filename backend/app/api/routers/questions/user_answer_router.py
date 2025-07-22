from fastapi import APIRouter, status, Depends

from app.api.controllers import UserAnswerController
from app.api.models import User
from app.api.utils.jwt_handler import get_current_user
from app.api.schemas import (
    UserAnswerQuery,
    UserAnswerListResponseSchema,
    UserAnswerResponseSchema,
    UserAnswerCreateSchema,
)

router = APIRouter(
    prefix="/user-answers",
    tags=["User Answers"],
)


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=UserAnswerListResponseSchema
)
async def list_(
    current_user: User = Depends(get_current_user),
    query: UserAnswerQuery = Depends(),
    user_answer_controller: UserAnswerController = Depends(),
) -> UserAnswerListResponseSchema:
    return await user_answer_controller.list_(query=query, user_id=current_user.id)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=UserAnswerResponseSchema
)
async def post(
    payload: UserAnswerCreateSchema,
    current_user: User = Depends(get_current_user),
    user_answer_controller: UserAnswerController = Depends(),
) -> UserAnswerResponseSchema:
    return await user_answer_controller.post(payload=payload, user_id=current_user.id)
