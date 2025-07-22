from fastapi import APIRouter

from .option_router import router as option_router
from .question_router import router as question_router
from .user_answer_router import router as user_answer_router

router = APIRouter()

router.include_router(option_router)
router.include_router(question_router)
router.include_router(user_answer_router)

__all__ = ["router"]
