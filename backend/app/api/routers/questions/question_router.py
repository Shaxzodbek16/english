from fastapi import APIRouter, status, Depends

from app.api.controllers import QuestionController

router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def list_():
    return ...


@router.get(
    "/{question_id}",
    status_code=status.HTTP_200_OK,
)
async def get(question_id: int):
    return ...


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def post(payload: dict):
    return ...


@router.put(
    "/{question_id}",
    status_code=status.HTTP_200_OK,
)
async def update(question_id: int, payload: dict):
    return ...


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(question_id: int):
    return ...
