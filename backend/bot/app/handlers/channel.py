from typing import Optional, Sequence
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from app.api.models import Channel
from bot.core.settings import Settings, get_settings


class ChannelRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self.settings: Settings = get_settings()
        self.bot: Bot = Bot(self.settings.BOT_TOKEN)

    async def create(self, channel_data: dict) -> Channel:
        channel = Channel(**channel_data)
        self.session.add(channel)
        await self.session.commit()
        await self.session.refresh(channel)
        return channel

    async def get_by_id(self, channel_id: int) -> Optional[Channel]:
        stmt = select(Channel).where(Channel.id == channel_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_channel_id(self, tg_channel_id: int) -> Optional[Channel]:
        stmt = select(Channel).where(Channel.channel_id == tg_channel_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Channel]:
        stmt = select(Channel).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, channel_id: int, update_data: dict) -> Optional[Channel]:
        channel = await self.get_by_id(channel_id)
        if not channel:
            return None
        channel.update(update_data)
        self.session.add(channel)
        await self.session.commit()
        await self.session.refresh(channel)
        return channel

    async def delete(self, channel_id: int) -> bool:
        stmt = delete(Channel).where(Channel.id == channel_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0  # noqa

    async def get_active_channels(self) -> Sequence[Channel]:
        stmt = select(Channel).where(Channel.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_expired_channels(self) -> Sequence[Channel]:
        stmt = select(Channel).where(Channel.is_active == True, Channel.till < datetime.utcnow())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def fetch_unsubscribed_channels(self, user_id: int, bot: Bot) -> Sequence[Channel]:
        unsubscribed_channels = []
        stmt = select(Channel).where(Channel.is_active == True, Channel.till > datetime.utcnow())
        result = await self.session.execute(stmt)
        all_channels = result.scalars().all()

        for channel in all_channels:
            try:
                member = await bot.get_chat_member(chat_id=channel.channel_id, user_id=user_id)
                if member.status not in ("member", "administrator", "creator"):
                    unsubscribed_channels.append(channel)
            except (TelegramBadRequest, TelegramForbiddenError):
                unsubscribed_channels.append(channel)
            except Exception:
                continue
        return unsubscribed_channels
