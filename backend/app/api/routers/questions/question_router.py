from fastapi import APIRouter, status, Depends

from app.api.controllers import QuestionController
from app.api.schemas import QuestionListResponseSchema, QueryParamsSchema

router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=QuestionListResponseSchema,
)
async def list_(
    query: QueryParamsSchema = Depends(),
    controller: QuestionController = Depends(QuestionController),
) -> QuestionListResponseSchema:
    return await controller.list_(query=query)


@router.get(
    "/{question_id}",
    status_code=status.HTTP_200_OK,
)
async def get(
    question_id: int,
):
    return ...


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def post(
    payload: dict,
):
    return ...


@router.put(
    "/{question_id}",
    status_code=status.HTTP_200_OK,
)
async def update(
    question_id: int,
    payload: dict,
):
    return ...


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    question_id: int,
):
    return ...
