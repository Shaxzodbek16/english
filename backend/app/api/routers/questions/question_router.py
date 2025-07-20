from fastapi import APIRouter, status, Depends, HTTPException

from app.api.controllers import QuestionController
from app.api.schemas import (
    QuestionListResponseSchema,
    QuestionQueryParamSchema,
    QuestionResponseSchema,
    QuestionCreateSchema,
    QuestionUpdateSchema,
)
from app.api.utils.jwt_handler import get_current_user

router = APIRouter(
    prefix="/questions", tags=["Questions"], dependencies=[Depends(get_current_user)]
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=QuestionListResponseSchema,
)
async def list_(
    query: QuestionQueryParamSchema = Depends(),
    controller: QuestionController = Depends(QuestionController),
) -> QuestionListResponseSchema:
    return await controller.list_(query=query)


@router.get(
    "/random",
    status_code=status.HTTP_200_OK,
    response_model=list[QuestionResponseSchema],
)
async def random(
    level_id: int = None,
    theme_id: int = None,
    limit: int = 30,
    question_controller: QuestionController = Depends(),
) -> list[QuestionResponseSchema]:
    if level_id is None or theme_id is None:
        if level_id < 1 or theme_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Both level_id and theme_id must be provided and greater than 0.",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either level_id and theme_id must be provided.",
        )
    if limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be a positive integer.",
        )
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must not exceed 100.",
        )
    return await question_controller.random(level_id, theme_id, limit)


@router.get(
    "/{question_id}",
    status_code=status.HTTP_200_OK,
    response_model=QuestionResponseSchema,
)
async def get(
    question_id: int, question_controller: QuestionController = Depends()
) -> QuestionResponseSchema:
    return await question_controller.get(question_id=question_id)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=QuestionResponseSchema
)
async def post(
    payload: QuestionCreateSchema, question_controller: QuestionController = Depends()
) -> QuestionResponseSchema:
    return await question_controller.post(payload=payload)


@router.put(
    "/{question_id}",
    status_code=status.HTTP_200_OK,
    response_model=QuestionResponseSchema,
)
async def update(
    question_id: int,
    payload: QuestionUpdateSchema,
    question_controller: QuestionController = Depends(),
) -> QuestionResponseSchema:
    return await question_controller.put(question_id=question_id, payload=payload)


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete(
    question_id: int,
    question_controller: QuestionController = Depends(),
) -> None:
    return await question_controller.delete(question_id=question_id)
