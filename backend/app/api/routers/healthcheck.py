from fastapi import APIRouter, status

router = APIRouter(
    prefix="/healthcheck",
    tags=["Health Check"],
)


@router.get("", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok", "message": "Service is running"}
