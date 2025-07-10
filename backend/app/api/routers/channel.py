from fastapi import APIRouter, status, Depends

from app.api.schemas import ChannelListResponseSchema, QueryParamsSchema
from app.core.settings import get_settings

settings = get_settings()

router = APIRouter(
    prefix="/channel",
    tags=["Channel"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ChannelListResponseSchema,
)
async def get_channel(
        params: QueryParamsSchema = Depends(),
) -> ChannelListResponseSchema:
    pass


@router.get(
    '/{channel_id}',
    status_code=status.HTTP_200_OK)
async def get_channel_by_id():
    return settings.base_dir
