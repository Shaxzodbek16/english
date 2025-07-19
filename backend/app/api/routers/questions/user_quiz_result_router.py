from fastapi import APIRouter, status, Depends

router = APIRouter(
    prefix="/user-quiz-results",
    tags=["User Quiz Results"],
)
