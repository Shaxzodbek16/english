from fastapi import APIRouter, status, Depends

router = APIRouter(
    prefix="/options",
    tags=["Options"],
)
