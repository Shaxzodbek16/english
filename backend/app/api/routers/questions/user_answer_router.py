from fastapi import APIRouter, status, Depends

router = APIRouter(
    prefix="/user-answers",
    tags=["User Answers"],
)
