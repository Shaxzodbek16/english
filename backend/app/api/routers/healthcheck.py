from fastapi import APIRouter, status

router = APIRouter()


@router.get("/healthcheck", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok", "message": "Service is running"}
