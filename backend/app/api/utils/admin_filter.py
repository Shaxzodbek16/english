from fastapi import Depends

from app.api.controllers import ChannelController
from app.api.models import User
from app.api.utils.jwt_handler import get_current_user


async def check_admin(
    user: User = Depends(get_current_user),
    channel_controller: ChannelController = Depends(),
):
    await channel_controller.check_admin(user)
