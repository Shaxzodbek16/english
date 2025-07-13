from fastapi import APIRouter, status, Depends

from app.api.controllers.channel_controller import ChannelController
from app.api.schemas import (
    ChannelListResponseSchema,
    QueryParamsSchema,
    CreateChannelSchema,
    UpdateChannelSchema,
    ChannelResponseSchema,
)
from app.api.utils.admin_filter import check_admin
from app.core.settings import get_settings

settings = get_settings()

router = APIRouter(
    prefix="/channel",
    tags=["Channel"],
    dependencies=[Depends(check_admin)],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ChannelListResponseSchema,
)
async def list_(
    params: QueryParamsSchema = Depends(),
    channel_controller: ChannelController = Depends(),
) -> ChannelListResponseSchema:
    return await channel_controller.list(params=params)


@router.get(
    "/{channel_id}",
    status_code=status.HTTP_200_OK,
    response_model=ChannelResponseSchema,
)
async def get(
    channel_id: int,
    channel_controller: ChannelController = Depends(),
):
    return await channel_controller.get(channel_id=channel_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ChannelResponseSchema,
    summary="It will multiply by -1 the channel_id.",
)
async def post(
    payload: CreateChannelSchema,
    channel_controller: ChannelController = Depends(),
):
    return await channel_controller.post(payload=payload)


@router.put(
    "/{channel_id}",
    status_code=status.HTTP_200_OK,
    response_model=ChannelResponseSchema,
)
async def put(
    channel_id: int,
    payload: UpdateChannelSchema,
    channel_controller: ChannelController = Depends(),
):
    return await channel_controller.put(channel_id=channel_id, payload=payload)


@router.delete(
    "/{channel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete(
    channel_id: int,
    channel_controller: ChannelController = Depends(),
):
    return await channel_controller.delete(channel_id=channel_id)
